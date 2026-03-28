---
name: enrich_people
description: Enrich person data using HSBinfo. Match on name, email, or address
method: POST,GET
endpoint: 

input_schema:
  type: object
  properties:
    name:
      type: string
      description: Full or partial name of the person

    email:
      type: string
      description: Email address

    address:
      type: string
      description: Address of the person

  additionalProperties: false
---

# Enrich People

Use this skill to retrieve enriched people data from the HSBinfo internal people database.

The API accepts:
- name
- email
- address

You can provide:
- only name
- only email
- only address
- any combination of the three

Returns best matching person record with score.