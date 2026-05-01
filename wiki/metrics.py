from typing import List
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModelForMaskedLM
from tqdm import tqdm
from torch.nn.functional import log_softmax
from mauve import compute_mauve

class Metric:
    def __init__(self, name='UnnamedMetric', device='cpu') -> None:
        self.name = name
        self.device = torch.device(device)

    def score(self, texts: List[str], refs: List[str]) -> float:
        raise NotImplementedError

class GPTPerplexityMetric(Metric):
    def __init__(self, model_str, name='UnnamedGPTPPLMetric', device='gpu') -> None:
        super().__init__(name, device)
        self.tokenizer = AutoTokenizer.from_pretrained(model_str)
        pad_id = self.tokenizer.encode(self.tokenizer.eos_token)[0]
        self.model = AutoModelForCausalLM.from_pretrained(model_str, return_dict=True, pad_token_id=pad_id).to(self.device)
    
    def score(self, texts: List[str], refs: List[str]) -> float:
        with torch.no_grad():
            nlls = []
            ppls = []
            lengths = []
            for i, text in enumerate(tqdm(texts, desc='perplexity')):
                input_ids = self.tokenizer.encode(text, return_tensors='pt', truncation=True).to(self.device)
                target_ids = input_ids.clone()
                try:
                    outputs = self.model(input_ids, labels=target_ids)
                except:
                    print('ppl model error')
                    print(f'text=<{text}>')
                    print(f'input_ids=<{input_ids}>')
                    print(f'index: {i}')
                    continue
                
                nll = outputs[0].cpu().detach()
                ppl = torch.exp(nll)
                length = input_ids.size(1)
                nlls.append(nll)
                ppls.append(ppl)
                lengths.append(length)
            nlls = torch.tensor(nlls).float()
            ppls = torch.tensor(ppls).float()
            lengths = torch.tensor(lengths).float()
            sent_avg_ppl = ppls.mean().item()

        return sent_avg_ppl

class MLMPerplexityMetric(Metric):
    def __init__(self, model_str, batch_size, name='UnnamedMLMPPLMetric', device='cpu') -> None:
        super().__init__(name, device)
        self.tokenizer = AutoTokenizer.from_pretrained(model_str)
        self.model = AutoModelForMaskedLM.from_pretrained(model_str).to(device)
        self.batch_size = batch_size
    
    def score(self, texts: List[str], refs: List[str]) -> float:
        ppls = []
        for i, text in enumerate(tqdm(texts, desc='mlm perplexity')):
            with torch.no_grad():
                input_ids = self.tokenizer.encode(text, return_tensors='pt', truncation=True).to(self.device) # (1, seqlen)
                seqlen = input_ids.size(-1)
                expanded_input_ids = input_ids.expand(seqlen, seqlen).clone() # (seqlen, seqlen), clone so that input_ids will not be changed by later operations
                masked_idxs = torch.arange(seqlen).to(self.device)
                expanded_input_ids[torch.arange(seqlen).to(self.device), masked_idxs] = self.tokenizer.mask_token_id # mask different positions for different copies
                
                orig_token_logprobs = []
                for b_idx in self.chunks(torch.arange(seqlen).to(self.device), self.batch_size):
                    b_masked_idxs = masked_idxs[b_idx] # (bz,)
                    b_orig_ids = input_ids[0][b_idx] # (bz,)
                    b_exp_input_ids = expanded_input_ids[b_idx, :]
                    out = self.model(input_ids=b_exp_input_ids)
                    token_logits = out.logits # (bz, seqlen, vocab_size)
                    token_logprobs = log_softmax(token_logits, dim=-1)
                    b_orig_token_logprobs = token_logprobs[torch.arange(b_idx.size(0)).to(self.device), b_masked_idxs, b_orig_ids] # extract position [i, b_masked_idxs[i], b_orig_ids[i]] for each i in batch (which is exactly the logprob of each masked position) (bz,)
                    orig_token_logprobs.append(b_orig_token_logprobs)
                orig_token_logprobs = torch.cat(orig_token_logprobs, dim=0) # score for each position (seqlen,)
                
                nll = orig_token_logprobs[1:-1].mean() # strip eos, bos
                ppl = torch.exp(-nll)

            ppls.append(ppl)
        ppls = torch.tensor(ppls).float()
        sent_avg_ppl = ppls.mean().item()

        return sent_avg_ppl
    
    def chunks(self, l, batch_size):
        return list(l[i:i + batch_size] for i in range(0, len(l), batch_size))

class MAUVEMetric(Metric):
    def __init__(self, model_str: str, max_text_length=512, name='UnnamedMAUVEMetric', device='cpu') -> None: # note: does not use pooler output
        super().__init__(name, device)
        self.featureize_model_name = model_str
        self.max_text_length = max_text_length
    
    def score(self, texts: List[str], refs: List[str]) -> float:
        gen = texts
        ref = refs
        if ref is None:
            return -1
        gen = [text.replace('[BOS]', '').replace('<|endoftext|>', '') for text in gen] # get rid of BOS, EOS
        gen = [text for text in gen if len(text) > 0]
        print(f'number of mauve generations: {len(gen)}')
        if len(ref) < len(gen): print('WARNING: MAUVE #reference < #generated! They should be the same!')
        if len(ref) > len(gen):
            print('MAUVE #reference > #generated, truncating reference to have length #generated')
            ref = ref[:len(gen)]
        out = compute_mauve(p_text=ref, q_text=gen, device_id=self.device.index, max_text_length=self.max_text_length, verbose=False, featurize_model_name=self.featureize_model_name)
        return out.mauve

#MAUVE_NAME_DICT = {
#    'gpt2': 'gpt2',
#    'roberta': 'roberta-base',
#    'electra': 'google/electra-large-discriminator'
#}
def get_metrics(
    metric_name_list: List[str],
    mlm_batch_size=64,
    mauve_maxlen=512,
    device='cpu',
    #use_base_models: bool = True
) -> List[Metric]:
    metrics_list = []

    #gpt_model = 'gpt2' if use_base_models else 'gpt2-large'
    #roberta_model = 'roberta-base' if use_base_models else 'roberta-large'
    #electra_model = 'google/electra-base-discriminator' if use_base_models else 'google/electra-large-discriminator'

    mauve_name_dict = {
        'gpt2': 'gpt2',
        'roberta': 'roberta-base',
        'roberta-large': 'roberta-large',
        'electra': 'google/electra-large-discriminator'
    }

    for name in metric_name_list:
        if name == 'gpt-ppl':
            metric = GPTPerplexityMetric(gpt_model, name, device)
        elif name == 'mlm-ppl':
            metric = MLMPerplexityMetric(roberta_model, mlm_batch_size, name, device)
        elif name.startswith('mauve-'):
            mauve_model_key = name[len('mauve-'):]
            model_name = mauve_name_dict.get(mauve_model_key)
            if model_name is None:
                raise NotImplementedError(f"Unknown model key: {mauve_model_key}")
            metric = MAUVEMetric(model_name, mauve_maxlen, name, device)
        else:
            raise NotImplementedError(f"Unknown metric: {name}")
        metrics_list.append(metric)

    return metrics_list