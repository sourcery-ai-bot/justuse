from packaging.version import Version as PkgVersion

class Version(PkgVersion):
    def __new__(cls, *args, **kwargs):
        if args and isinstance(args[0], Version):
            return args[0]
        else:
            return super(cls, Version).__new__(cls)

    def __init__(self, versionstr=None, *, major=0, minor=0, patch=0):
        if isinstance(versionstr, Version):
            return
        if not (versionstr or major or minor or patch):
            raise ValueError(
                "Version must be initialized with either a string or major, minor and patch"
            )
        if major or minor or patch:
            # string as only argument, no way to construct a Version otherwise - WTF
            return super().__init__(".".join((str(major), str(minor), str(patch))))
        return super().__init__(versionstr)

    def __iter__(self):
        yield from self.release

    def __repr__(self):
        return f"use.Version({'.'.join(map(str,self.release))!r})"


v = Version(Version("1"))
print(v)
v2 = Version(Version(major=2, minor=0))