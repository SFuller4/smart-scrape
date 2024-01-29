import bittensor as bt
import argparse
import os
from distutils.util import strtobool
import torch

def str2bool(v):
    return bool(strtobool(v))


def check_config(cls, config: "bt.Config"):
    bt.axon.check_config(config)
    bt.logging.check_config(config)
    full_path = os.path.expanduser(
        "{}/{}/{}/{}".format(
            config.logging.logging_dir,
            config.wallet.get("name", bt.defaults.wallet.name),
            config.wallet.get("hotkey", bt.defaults.wallet.hotkey),
            config.miner.name,
        )
    )
    config.miner.full_path = os.path.expanduser(full_path)
    if not os.path.exists(config.miner.full_path):
        os.makedirs(config.miner.full_path)


def get_config() -> "bt.Config":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--axon.port", type=int, default=8098, help="Port to run the axon on."
    )
    # Subtensor network to connect to
    parser.add_argument(
        "--subtensor.network",
        default="finney",
        help="Bittensor network to connect to.",
    )
    # Chain endpoint to connect to
    parser.add_argument(
        "--subtensor.chain_endpoint",
        default="wss://entrypoint-finney.opentensor.ai:443",
        help="Chain endpoint to connect to.",
    )
    # Adds override arguments for network and netuid.
    parser.add_argument("--netuid", type=int, default=22, help="The chain subnet uid.")

    parser.add_argument(
        "--miner.root",
        type=str,
        help="Trials for this miner go in miner.root / (wallet_cold - wallet_hot) / miner.name ",
        default="~/.bittensor/miners/",
    )
    parser.add_argument(
        "--miner.name",
        type=str,
        help="Trials for this miner go in miner.root / (wallet_cold - wallet_hot) / miner.name ",
        default="Bittensor Miner",
    )

    # Run config.
    parser.add_argument(
        "--miner.blocks_per_epoch",
        type=str,
        help="Blocks until the miner sets weights on chain",
        default=100,
    )

    # Mocks.    
    parser.add_argument(
        "--miner.mock_dataset",
        type=str2bool,
        help="If True, the miner will retrieve data from mock dataset",
        default=False
    )
 
    parser.add_argument(
        "--miner.intro_text",
        type=str2bool,
        help="If True, the miner will return intro text",
        default=True
    )

    parser.add_argument(
        "--miner.device",
        type=str,
        help="Device to run the validator on.",
        default="cuda" if torch.cuda.is_available() else "cpu",
    )

    parser.add_argument(
        "--llm.model_provider",
        type=str,
        default="openai",
        help="The provider of the language model. Options are 'openai' for OpenAI models, 'local' for local models.",
    )

    parser.add_argument(
        "--llm.model_name",
        type=str,
        default="gpt-3.5-turbo-1106",
        help="Name/path of model to load. Also can be a filepath to the model weights (HF)",
    )

    parser.add_argument(
        "--llm.temperature",
        type=float,
        help="Sampling temperature of model",
        default=0.2,
    )

    parser.add_argument(
        "--llm.summary_model",
        default="gpt-3.5-turbo-1106",
        help="LLM name used for summarizing content.",
    )

    parser.add_argument(
        "--llm.query_model",
        default="gpt-3.5-turbo-1106",
        help="LLM name used for generating queries.",
    )

    parser.add_argument(
        "--llm.fix_query_model",
        default="gpt-4-1106-preview",
        help="LLM name used for fixing queries.",
    )

    # Adds subtensor specific arguments i.e. --subtensor.chain_endpoint ... --subtensor.network ...
    bt.subtensor.add_args(parser)

    # Adds logging specific arguments i.e. --logging.debug ..., --logging.trace .. or --logging.logging_dir ...
    bt.logging.add_args(parser)

    # Adds wallet specific arguments i.e. --wallet.name ..., --wallet.hotkey ./. or --wallet.path ...
    bt.wallet.add_args(parser)

    # Adds axon specific arguments i.e. --axon.port ...
    bt.axon.add_args(parser)

    # Activating the parser to read any command-line inputs.
    # To print help message, run python3 template/miner.py --help
    config = bt.config(parser)

    # Logging captures events for diagnosis or understanding miner's behavior.
    config.full_path = os.path.expanduser(
        "{}/{}/{}/netuid{}/{}".format(
            config.logging.logging_dir,
            config.wallet.name,
            config.wallet.hotkey,
            config.netuid,
            "miner",
        )
    )
    # Ensure the directory for logging exists, else create one.
    if not os.path.exists(config.full_path):
        os.makedirs(config.full_path, exist_ok=True)
    return config