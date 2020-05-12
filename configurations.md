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
* Code: topic_creation_lambda.py

### DeleteSNSTopic function

* Runtime: Python 3.8
* Role name: Lambda_Delete_SNS_Topic_Role
* Code: topic_deletion_lambda.py

### SubscribeToSNSTopic function

* Runtime: Python 3.8
* Role name: Lambda_Manage_SNS_Subscriptions_Role
* Code: subscription_creation_lambda.py

### UnsubscribeFromSNSTopic function

* Runtime: Python 3.8
* Role name: Lambda_Manage_SNS_Subscriptions_Role
* Code: subscription_deletion_lambda.py


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

## Roles

### Lambda_Add_SNS_Topic_Role
* Name: Lambda_Add_SNS_Topic_Role
* Description: Allows Lambda to add an item to the SNS_Subscriptions table, which logically would represent a new SNS topic, and query existing items (in order to see if topic name is already taken)
* Use case: Lambda
* Permissions: SNS_Subscriptions_Add_Topic_Policy, SNS_Subscriptions_Query_Topics_Policy

### Lambda_Delete_SNS_Topic_Role
* Name: Lambda_Delete_SNS_Topic_Role
* Description: Allows Lambda to delete an item from the SNS_Subscriptions table, which logically represents deleting a SNS topic
* Use case: Lambda
* Permissions: SNS_Subscriptions_Delete_Topic_Policy

### Lambda_Manage_SNS_Subscriptions_Role
* Name: Lambda_Manage_SNS_Subscriptions_Role
* Description: Allows lambda to access and modify SNS_Subscription items, which logically represent SNS subscriptions to a certain SNS topic
* Use case: Lambda
* Permissions: SNS_Subscriptions_Get_Topic_Policy, SNS_Subscriptions_Update_Topic_Policy


