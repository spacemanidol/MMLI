from transformers import LongformerModel
model = LongformerModel.from_pretrained('allenai/longformer-base-4096', gradient_checkpointing=True)