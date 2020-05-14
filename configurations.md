## DynamoDB configurations

### Topics table

* Table name: SNS_Subscriptions
* Primary key: topic

Structure of the items:
Topic - topic name, must be unique
Subscriptions - map of the following shape:

```javascript
{
    "SQS": [
        // list of subscribed SQS ARNs 
    ],
    "Lambda": [
        // list of subscribed Lambda ARNs
    ]
    "Email": [
        // list of emails
    ],
    "HTTP": [
        // list of HTTP endpoints
    ]
}
```

## Lambda configurations

### CreateSNSTopic function

* Runtime: Python 3.8
* Role name: Lambda_Add_SNS_Topic_Role
* Code: [topic_creation_lambda.py](topic_creation_lambda.py)

### DeleteSNSTopic function

* Runtime: Python 3.8
* Role name: Lambda_Delete_SNS_Topic_Role
* Code: [topic_deletion_lambda.py](topic_deletion_lambda.py)

### SubscribeToSNSTopic function

* Runtime: Python 3.8
* Role name: Lambda_Manage_SNS_Subscriptions_Role
* Code: [subscription_creation_lambda.py](subscription_creation_lambda.py)

### UnsubscribeFromSNSTopic function

* Runtime: Python 3.8
* Role name: Lambda_Manage_SNS_Subscriptions_Role
* Code: [subscription_deletion_lambda.py](subscription_deletion_lambda.py)

### SNSSendEmail function

* Runtime: Python 3.8
* Role name: Lambda_Send_Subscription_Emails_Role
* Code: [send_email_lambda.py](send_email_lambda.py)
* Environment variables:
    * EMAIL_SENDER (Name <some-email@example.com>)
    * EMAIL_SERVER_REGION (valid AWS region name)
* Helper environment variables: (For testing with the aws account)
    * SENDER_ACCESS_KEY
    * SENDER_SECRET_ACCESS_KEY

### SNSSendSQSMessage function

* Runtime: Python 3.8
* Role name: Lambda_Send_SQS_Message_Role
* Code: [send_sqs_message_lambda.py](send_sqs_message_lambda.py)

### SNSInvokeLambdas function

* Runtime: Python 3.8
* Role name: Lambda_Invoke_Lambda_Role
* Code: [invoke_lambdas_lambda.py](invoke_lambdas_lambda.py)

### SendMessageToSNSTopic function

* Runtime: Python 3.8
* Role name: Lambda_Send_Messages_For_Topic_Role
* Code: [send_message_to_topic_lambda.py](send_message_to_topic_lambda.py)

### SNSMakeHTTPRequest function

* Runtime: Python 3.8
* Role name: Lambda_Empty_Role
* Code: [make_http_request_lambda.py](make_http_request_lambda.py)

## Policies

### SNS_Subscriptions_Add_Topic_Policy

* Name: SNS_Subscriptions_Add_Topic_Policy
* Description: Allows principal to add an item to the SNS_Subscriptions table, which logically would represent a new SNS topic.
* Service: DynamoDB
* Action: PutItem
* Resources: Specific: SNS_Subscriptions table ARN
* JSON:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": "dynamodb:PutItem",
            "Resource": "arn:aws:dynamodb:us-east-1:618803543352:table/SNS_Subscriptions"
        }
    ]
}
```

### SNS_Subscriptions_Delete_Topic_Policy

* Description: Allows principal to delete an item from the SNS_Subscriptions table, which logically represents deleting a SNS topic
* Service: DynamoDB
* Action: DeleteItem
* Resources: Specific: SNS_Subscriptions table ARN
* JSON:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": "dynamodb:DeleteItem",
            "Resource": "arn:aws:dynamodb:us-east-1:618803543352:table/SNS_Subscriptions"
        }
    ]
}
```

### SNS_Subscriptions_Update_Topic_Policy

* Description: Allows principal to update an item in the SNS_Subscriptions table, which means modifying the subscriptions for a certain SNS topic
* Service: DynamoDB
* Action: UpdateItem
* Resources: Specific: SNS_Subscriptions table ARN
* JSON:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": "dynamodb:UpdateItem",
            "Resource": "arn:aws:dynamodb:us-east-1:618803543352:table/SNS_Subscriptions"
        }
    ]
}
```

### SNS_Subscriptions_Get_Topic_Policy

* Description: Allows principal to get an item from the SNS_Subscriptions table, which means accessing the subscriptions for a certain SNS topic
* Service: DynamoDB
* Action: GetItem
* Resources: Specific: SNS_Subscriptions table ARN
* JSON:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": "dynamodb:GetItem",
            "Resource": "arn:aws:dynamodb:us-east-1:618803543352:table/SNS_Subscriptions"
        }
    ]
}
```

### SNS_Subscriptions_Query_Topics_Policy

* Name: SNS_Subscriptions_Query_Topics_Policy
* Description: Allows principal to query items from the SNS_Subscriptions table, which logically represent SNS topics.
* Service: DynamoDB
* Action: Query
* Resources: Specific: 
    * table: SNS_Subscriptions table ARN
    * index: any

### SES_Send_Emails_Policy

* Name: SES_Send_Emails_Policy
* Description: Allows principal to send emails
* Service: SES
* Action: SendEmail
* Resources: All resources
* JSON:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": "ses:SendEmail",
            "Resource": "*"
        }
    ]
}
```

### SQS_Send_Message_Policy
* Name: SQS_Send_Message_Policy
* Description: Allows principal to send SQS messages
* Service: SQS
* Action: SendMessage
* Resources: All resources
* JSON:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": "sqs:SendMessage",
            "Resource": "*"
        }
    ]
}
```

### Lambda_Invoke_Policy
* Name: Lambda_Invoke_Policy
* Description: Allows principal to invoke lambdas
* Service: Lambda
* Action: InvokeFunction
* Resources: All resources
* JSON:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": "lambda:InvokeFunction",
            "Resource": "*"
        }
    ]
}
```

### Invoke_Message_Sending_Lambdas_Policy
* Name: Invoke_Message_Sending_Lambdas_Policy
* Description: Allows principal to invoke the lambdas which send messages for each type of subscription entity supported
* Service: Lambda
* Action: InvokeFunction
* Resources: Specific: 
    * The ARN of SNSSendEmail lambda
    * The ARN of SNSSendSQSMessage lambda
    * The ARN of SNSInvokeLambdas lambda
* JSON:

## Roles

### Lambda_Add_SNS_Topic_Role
* Name: Lambda_Add_SNS_Topic_Role
* Description: Allows Lambda to add an item to the SNS_Subscriptions table, which logically would represent a new SNS topic
* Use case: Lambda
* Permissions: SNS_Subscriptions_Add_Topic_Policy

### Lambda_Delete_SNS_Topic_Role
* Name: Lambda_Delete_SNS_Topic_Role
* Description: Allows Lambda to delete an item from the SNS_Subscriptions table, which logically represents deleting a SNS topic
* Use case: Lambda
* Permissions: SNS_Subscriptions_Delete_Topic_Policy

### Lambda_Modify_SNS_Subscriptions_Role
* Name: Lambda_Manage_SNS_Subscriptions_Role
* Description: Allows lambda to modify SNS_Subscription items, which logically represent SNS subscriptions to a certain SNS topic
* Use case: Lambda
* Permissions: SNS_Subscriptions_Update_Topic_Policy

### Lambda_Read_Topic_Subscriptions_Role
* Name: Lambda_Read_Topic_Subscriptions_Role
* Description: Allows lambda to get items from the SNS_Subscription table, which logically represent SNS subscriptions to a certain SNS topic
* Use case: Lambda
* Permissions: SNS_Subscriptions_Get_Topic_Policy

### Lambda_Send_Subscription_Emails_Role
* Name: Lambda_Read_Topic_Subscriptions_Role
* Description: Allows lambda to send emails
* Use case: Lambda
* Permissions: SES_Send_Emails_Policy

### Lambda_Send_SQS_Message_Role
* Name: Lambda_Send_SQS_Message_Role
* Description: Allows lambda to send SQS messages
* Use case: Lambda
* Permissions: SQS_Send_Message_Policy

### Lambda_Invoke_Lambda_Role
* Name: Lambda_Invoke_Lambda_Role
* Description: Allows lambda to invoke lambdas
* Use case: Lambda
* Permissions: Lambda_Invoke_Policy

### Lambda_Send_Messages_For_Topic_Role
* Name: Lambda_Send_Messages_For_Topic_Role
* Description: Allows lambda to read subscriptions for a certain topic from the SNS_Subscriptions table and in turn invoke the lambdas which send messages for each type of subscription entity supported
* Use case: Lambda
* Permissions: SNS_Subscriptions_Get_Topic_Policy, Invoke_Message_Sending_Lambdas_Policy

### Lambda_Empty_Role
* Name: Lambda_Empty_Role
* Description: Denies lambda access to any resources
* Use case: Lambda
* Permissions: None

