# scripts/test_logging.py

import torch
import torch.nn as nn
import torch.optim as optim
import wandb

from swizz.logging.logger import LogTracker, log

def main():
    # 1) Initialize W&B
    wandb.init(
        project="swizz_test",
        name="simple_test",
        config={
            "n_epochs": 3,
            "batches_per_epoch": 5,
            "batch_size": 16,
            "learning_rate": 0.1,
        },
    )
    run_name = wandb.run.name  # group local logs under this

    # 2) Build a simple linear model + MSE loss
    model = nn.Linear(10, 1)
    optimizer = optim.SGD(model.parameters(), lr=wandb.config.learning_rate)
    loss_fn = nn.MSELoss()

    n_epochs = wandb.config.n_epochs
    batches_per_epoch = wandb.config.batches_per_epoch
    batch_size = wandb.config.batch_size

    # 3) Set up our logging trackers
    #    Now we trigger whenever "epoch" appears in logs (i.e. every epoch)
    epoch_tracker = LogTracker(
        name="epoch",
        counter_key="epoch",
        final_idx=n_epochs,
        keys_to_log=["epoch"],
        add_first=True,
        add_last=True,
    )
    #    Trigger whenever "loss" appears (i.e. every batch), but only if epoch_tracker fired
    batch_tracker = LogTracker(
        name="batch",
        counter_key="batch",
        final_idx=batches_per_epoch,
        keys_to_log=["loss"],
        depends_on=epoch_tracker,
        add_first=True,
        add_last=True,
    )

    # 4) Training loop
    for epoch in range(n_epochs):
        # Prepare epoch‐level metrics
        epoch_metrics = {
            "epoch": epoch,
            "dummy_epoch_metric": float(epoch) / n_epochs,
        }
        # Register and log if any of keys_to_log fired
        if epoch_tracker.register(epoch, epoch_metrics):
            # This writes both to wandb and to swizz_runs/<run_name>/
            log(epoch_metrics, run_name=run_name)

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

            # Prepare batch‐level metrics
            batch_metrics = {
                "epoch": epoch,
                "batch": batch_idx,
                "loss": loss.item(),
            }
            # Register and log
            if batch_tracker.register(batch_idx, batch_metrics):
                log(batch_metrics, run_name=run_name)

    print("Done training. Check wandb and swizz_runs/… folders.")

if __name__ == "__main__":
    main()
