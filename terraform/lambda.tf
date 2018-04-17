variable "python_version" {
  default = "2.7"
}
variable "prefix" {
  default = ""
}
variable "subnet_ids" {
  default = ""
}
variable "lambda_role_arn" {
  default = ""
}
variable "endpoint" {
  default = ""
}
variable "index_prefix" {
  default = "logstash"
}
variable "delete_after" {
  default = ""
}
variable "timestring" {
  default = ""
}
variable "tags" {
  type = "map"
  default = {
    Name = "es-grooming"
  }
}
data "archive_file" "es_grooming_lambda" {
  type        = "zip"
  source_dir  = "${path.module}/src/"
  output_path = "${path.module}/es-grooming.zip"
}

resource "aws_lambda_function" "es_grooming" {
  count            = "${length(var.subnet_ids) == 0 ? 1 : 0}"
  filename         = "${path.module}/es-grooming.zip"
  function_name    = "${var.prefix}es_grooming"
  description      = "${var.prefix}es_grooming"
  timeout          = 300
  runtime          = "python${var.python_version}"
  role             = "${var.lambda_role_arn}"
  handler          = "index.handler"
  source_code_hash = "${data.archive_file.es_grooming_lambda.output_base64sha256}"

  environment {
    variables = {
      endpoint  = "${var.endpoint}"
      prefix        = "${var.index_prefix}"
      delete_after = "${var.delete_after}"
      timestring = "${var.timestring}"
    }
  }
}