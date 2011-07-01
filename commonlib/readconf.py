import copy
import commonlib.helpers

odict = commonlib.helpers.odict

def parse_config(conf_default, conf_local=None):
    config = odict(**copy.deepcopy(conf_default.config))
    if conf_local:
        local_config = conf_local.config
        for section in config:
            local_config_section = local_config.get(section)
            if local_config_section:
                if isinstance(local_config_section, dict):
                    config[section].update(local_config_section)
                else:
                    config[section] = local_config_section
    return config

