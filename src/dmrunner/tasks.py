from invoke import Collection

import check
import code
import config
import data

namespace = Collection(config, check, code, data)
