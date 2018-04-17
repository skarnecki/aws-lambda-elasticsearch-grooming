# aws-lambda-elasticsearch-grooming
AWS lambda that trims old indices

### Lambda configuration

| Variable Name | Example Value | Description | Default Value | Required |
| --- | --- | --- | --- |  --- |
| endpoint | https://your-es.com  | Elasticsearch Address | `None` | True |
| index_prefix |  `logstash,cwl` | index prefix | `logstash` | False |
| timestring  | `%Y.%m-%d` | Combined with `index` variable is used to evaluate the index age | `%Y-%m-%d` |  False |
| delete_after | `14` | Numbers of days to preserve | `15` |  False |
| python_version | `2.7` | Version of Python used for lambda | `2.7` | False |
| prefix | `myapp` | Prefix for lambda function | ` ` | False |
| subnet_ids | `subnet-2fd8c858,subnet-f5c6e9ac` | List of subnet ids for VPC deployed Lambda. Empty means Lambda not in VPC | ` ` | False |
| lambda_role_arn | `arn:aws:iam::123123123:role/lambda-es-grooming` | Lambda Role arn | ` ` | True |
