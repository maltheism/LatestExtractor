#!/usr/bin/env python

from libs import config, plugin

# disables print depending on settings.
config.Settings.debugger()

# plugin: DataLad extractor.
extractor = plugin.Extractor()

# refresh annex data for extractor.
extractor.refresh()

# process extractor data.
#extractor.process()
