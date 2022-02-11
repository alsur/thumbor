#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/thumbor/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com thumbor@googlegroups.com

from thumbor.loaders import LoaderResult, file_loader, http_loader
from tornado.concurrent import return_future


@return_future
def load(context, path, callback):
    def callback_wrapper(result):
        if result.successful:
            callback(result)
        else:
            if not http_loader.validate(context, path):
                result = LoaderResult()
                result.successful = False
                result.error = LoaderResult.ERROR_BAD_REQUEST
                result.extras["reason"] = "Unallowed domain"
                result.extras["source"] = path

                return result
            # If file_loader failed try http_loader
            http_loader.load(context, path, callback)

    # First attempt to load with file_loader
    file_loader.load(context, path, callback_wrapper)
