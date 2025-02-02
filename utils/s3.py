import boto3
import datetime


class SSMParameterStore(object):
    """
    Provide a dictionary-like interface to access AWS SSM Parameter Store
    """

    def __init__(self, prefix=None, ssm_client=None, ttl=None):
        self._prefix = (prefix or "").rstrip("/") + "/"
        self._client = ssm_client or boto3.client("ssm", region_name="us-west-2")
        self._keys = None
        self._substores = {}
        self._ttl = ttl

    def get(self, name, **kwargs):
        assert name, "Name can not be empty"
        if self._keys is None:
            self.refresh()

        abs_key = "%s%s" % (self._prefix, name)
        if name not in self._keys:
            if "default" in kwargs:
                return kwargs["default"]

            raise KeyError(name)
        elif self._keys[name]["type"] == "prefix":
            if abs_key not in self._substores:
                store = self.__class__(
                    prefix=abs_key, ssm_client=self._client, ttl=self._ttl
                )
                store._keys = self._keys[name]["children"]
                self._substores[abs_key] = store

            return self._substores[abs_key]
        else:
            return self._get_value(name, abs_key)

    def refresh(self):
        self._keys = {}
        self._substores = {}

        paginator = self._client.get_paginator("describe_parameters")
        pager = paginator.paginate(
            ParameterFilters=[
                dict(Key="Path", Option="Recursive", Values=[self._prefix])
            ]
        )

        for page in pager:
            for p in page["Parameters"]:
                paths = p["Name"][len(self._prefix) :].split("/")
                self._update_keys(self._keys, paths)

    @classmethod
    def _update_keys(cls, keys, paths):
        name = paths[0]

        # this is a prefix
        if len(paths) > 1:
            if name not in keys:
                keys[name] = {"type": "prefix", "children": {}}

            cls._update_keys(keys[name]["children"], paths[1:])
        else:
            keys[name] = {"type": "parameter", "expire": None}

    def keys(self):
        if self._keys is None:
            self.refresh()

        return self._keys.keys()

    def _get_value(self, name, abs_key):
        entry = self._keys[name]

        # simple ttl
        if not self._ttl or (
            entry["expire"] and entry["expire"] <= datetime.datetime.now()
        ):
            entry.pop("value", None)

        if "value" not in entry:
            parameter = self._client.get_parameter(Name=abs_key, WithDecryption=True)[
                "Parameter"
            ]
            value = parameter["Value"]
            if parameter["Type"] == "StringList":
                value = value.split(",")

            entry["value"] = value

            if self._ttl:
                entry["expire"] = datetime.datetime.now() + datetime.timedelta(
                    seconds=self._ttl
                )
            else:
                entry["expire"] = None

        return entry["value"]

    def __contains__(self, name):
        try:
            self.get(name)
            return True
        except KeyError:
            return False

    def __getitem__(self, name):
        return self.get(name)

    def __setitem__(self, key, value):
        raise NotImplementedError()

    def __delitem__(self, name):
        raise NotImplementedError()

    def __repr__(self):
        return "ParameterStore[%s]" % self._prefix
