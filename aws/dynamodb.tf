resource "aws_dynamodb_table" "connections" {
    name            = "connections"
    billing_mode    = "PAY_PER_REQUEST"
    hash_key        = "nodeID"
    range_key        = "connectionTime"

    attribute {
        name = "nodeID"
        type = "S"
    }

    attribute {
        name = "connectionTime"
        type = "S"
    }
}
