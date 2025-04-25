# scripts/test_logging.py

import torch
import torch.nn as nn
import torch.optim as optim
import wandb

from paperviz.logging.logging import LogTracker, log, filter_out_underscore, filter_out_wandb

def main():
    # 1) Initialize W&B
    wandb.init(
        project="paperviz_test",
        name="simple_test",
        config={
            "n_epochs": 3,
            "batches_per_epoch": 5,
            "batch_size": 16,
            "learning_rate": 0.1,
        },
    )

    # 2) Build a simple linear model + MSE loss
    model = nn.Linear(10, 1)
    optimizer = optim.SGD(model.parameters(), lr=wandb.config.learning_rate)
    loss_fn = nn.MSELoss()

    n_epochs = wandb.config.n_epochs
    batches_per_epoch = wandb.config.batches_per_epoch
    batch_size = wandb.config.batch_size

    # 3) Set up our logging trackers
    epoch_tracker = LogTracker(
        name="epoch",
        counter_key="epoch",
        trigger_level=LogTracker.EPOCH,
        logging_level=LogTracker.EPOCH,   # log every epoch
        final_idx=n_epochs,
        add_first=True,
        add_last=True,
    )
    batch_tracker = LogTracker(
        name="batch",
        counter_key="batch",
        trigger_level=LogTracker.BATCH,
        logging_level=20,                  # log every ~5% of batches
        final_idx=batches_per_epoch,
        depends_on=epoch_tracker,          # only log batches when epoch tracker fires
        add_first=True,
        add_last=True,
    )

    # 4) Training loop
    for epoch in range(n_epochs):
        # register & possibly log at epoch granularity
        epoch_tracker.register_progress(epoch)
        if epoch_tracker.log_this_round:
            epoch_metrics = {
                "epoch": epoch,
                "dummy_epoch_metric": float(epoch) / n_epochs,
            }
            # ─── write locally under paperviz_runs/epoch/… ───
            epoch_tracker.log_to_file(filter_out_wandb(epoch_metrics))
            # ─── log to wandb ───
            wandb.log(filter_out_underscore(epoch_metrics))

        for batch_idx in range(batches_per_epoch):
            # create random data
            x = torch.randn(batch_size, 10)
            y = torch.randn(batch_size, 1)

            # forward / backward
            preds = model(x)
            loss = loss_fn(preds, y)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            # register & possibly log at batch granularity
            progress = 1.0 / batches_per_epoch
            batch_tracker.register_progress(batch_idx, progress)
            if batch_tracker.log_this_round:
                batch_metrics = {
                    "epoch": epoch,
                    "batch": batch_idx,
                    "loss": loss.item(),
                }
                # ─── write locally under paperviz_runs/batch/… ───
                batch_tracker.log_to_file(filter_out_wandb(batch_metrics))
                # ─── log to wandb ───
                wandb.log(filter_out_underscore(batch_metrics))

    print("Done training. Check wandb and the paperviz_runs/… folders.")

if __name__ == "__main__":
    main()
