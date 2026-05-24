PRODUCT_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "id": {
            "type": "integer",
            "minimum": 1
        },
        "title": {
            "type": "string",
            "minLength": 1
        },
        "description": {
            "type": "string",
            "minLength": 1
        },
        "category": {
            "type": "string",
            "minLength": 1
        },
        "price": {
            "type": "number",
            "exclusiveMinimum": 0
        },
        "discountPercentage": {
            "type": "number",
            "minimum": 0,
            "maximum": 100
        },
        "rating": {
            "type": "number",
            "minimum": 0,
            "maximum": 5
        },
        "stock": {
            "type": "integer",
            "minimum": 0
        },
        "tags": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "string",
                "minLength": 1
            }
        },
        "brand": {
            "type": "string",
            "minLength": 1
        },
        "sku": {
            "type": "string",
            "minLength": 1
        },
        "weight": {
            "type": "integer",
            "exclusiveMinimum": 0
        },
        "dimensions": {
            "type": "object",
            "properties": {
                "width": {
                    "type": "number",
                    "exclusiveMinimum": 0
                },
                "height": {
                    "type": "number",
                    "exclusiveMinimum": 0
                },
                "depth": {
                    "type": "number",
                    "exclusiveMinimum": 0
                }
            },
            "required": ["width", "height", "depth"]
        },
        "warrantyInformation": {
            "type": "string",
            "minLength": 1
        },
        "shippingInformation": {
            "type": "string",
            "minLength": 1
        },
        "availabilityStatus": {
            "type": "string",
            "minLength": 1
        },
        "reviews": {
            "type": "array",
            "minItems": 0,
            "items": {
                "type": "object",
                "properties": {
                    "rating": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 5
                    },
                    "comment": {
                        "type": "string",
                        "minLength": 1
                    },
                    "date": {
                        "type": "string",
                        "format": "date-time"
                    },
                    "reviewerName": {
                        "type": "string",
                        "minLength": 1
                    },
                    "reviewerEmail": {
                        "type": "string",
                        "format": "email"
                    }
                },
                "required": ["rating", "comment", "date", "reviewerName", "reviewerEmail"]
            }
        },
        "returnPolicy": {
            "type": "string",
            "minLength": 1
        },
        "minimumOrderQuantity": {
            "type": "integer",
            "minimum": 1
        },
        "meta": {
            "type": "object",
            "properties": {
                "createdAt": {
                    "type": "string",
                    "format": "date-time"
                },
                "updatedAt": {
                    "type": "string",
                    "format": "date-time"
                },
                "barcode": {
                    "type": "string",
                    "minLength": 1
                },
                "qrCode": {
                    "type": "string",
                    "minLength": 1
                }
            },
            "required": ["createdAt", "updatedAt", "barcode", "qrCode"]
        },
        "thumbnail": {
            "type": "string",
            "format": "uri"
        },
        "images": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "string",
                "format": "uri"
            }
        }
    },
    "required": [
        "id", "title", "description", "category", "price",
        "discountPercentage", "rating", "stock", "tags",
        "sku", "weight", "dimensions", "reviews",
        "returnPolicy", "minimumOrderQuantity", "meta", "thumbnail", "images"
    ]
}