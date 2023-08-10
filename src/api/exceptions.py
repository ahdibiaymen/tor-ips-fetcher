class ValidationError(Exception):
    def __init__(self, **errors):
        self.message = "Validation Error :"
        if errors:
            self.message += f": {errors}"
        super().__init__(self.message)


class AlreadyExists(Exception):
    def __init__(self, **errors):
        self.message = "Resource already exists"
        if errors:
            self.message += f": {errors}"
        super().__init__(self.message)


class DBError(Exception):
    def __init__(self, **errors):
        self.message = "Something went in I/O database operation"
        if errors:
            self.message += f": {errors}"
        super().__init__(self.message)


class BadRemoteURL(Exception):
    def __init__(self, **errors):
        self.message = "Remote URL doesn't exist"
        if errors:
            self.message += f": {errors}"
        super().__init__(self.message)


class RemoteURLContentChanged(Exception):
    def __init__(self, **errors):
        self.message = "Remote URL content has been changed"
        if errors:
            self.message += f": {errors}"
        super().__init__(self.message)


class NotFound(Exception):
    def __init__(self, **errors):
        self.message = "Resource not found"
        if errors:
            self.message += f": {errors}"
        super().__init__(self.message)
