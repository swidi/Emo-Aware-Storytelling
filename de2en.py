from fairseq.models.transformer import TransformerModel
zh2en = TransformerModel.from_pretrained(
  '/home/marcel/fairseq/examples/translation/wmt19.de-en.joined-dict.ensemble/',
  checkpoint_file='checkpoint_best.pt',
  data_name_or_path='data-bin/wmt17_zh_en_full',
  bpe='subword_nmt',
  bpe_codes='data-bin/wmt17_zh_en_full/zh.code'
)
zh2en.translate('你好 世界')