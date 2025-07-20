from _pytest.config import Config
from _pytest.main import Session
from _pytest.nodes import Item


def pytest_addoption(parser):
    parser.addoption(
        "--ekstazi",
        action="store_true",
        help="select tests using ekstazi test selection",
    )


# hook called after pytest collection has been performed
def pytest_collection_modifyitems(session: Session, config: Config, items: list[Item]):
    print("Ekstazi loaded")
    print("listing tests:")
    for item in items:
        print(item.name)
