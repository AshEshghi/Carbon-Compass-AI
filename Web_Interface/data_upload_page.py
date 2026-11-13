
class DataUploadPage:
    def __init__(self, file_name):
        self.file_name = file_name
        self.validation_result = None

    def get_file_name(self):
        return self.file_name

    def set_file_name(self, file_name):
        self.file_name = file_name

    def get_validation_result(self):
        return self.validation_result

    def set_validation_result(self, result):
        self.validation_result = result

    def render_upload(self):
        return "Uploaded file: " + self.file_name

    def render_validation(self):
        if self.validation_result is None:
            return "Validation has not been performed yet."

        valid_records = self.validation_result["valid_records"]
        errors = self.validation_result["errors"]

        return {
            "valid_count": len(valid_records),
            "error_count": len(errors),
            "errors": errors
        }


# Test the class
if __name__ == "__main__":
    upload = DataUploadPage("electricity.csv")

    print(upload.render_upload())
    print(upload.render_validation())
