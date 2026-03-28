## enrich_people



description: >
Enrich a person profile using fuzzy matching on name, email, or address.
Returns the best matching person if confidence is high.

endpoint: https://YOUR-RENDER-URL.onrender.com/skills/enrich_people

method: POST

headers:
  Content-Type: application/json

input_schema:

  type: object

  properties:(any one or combination of fields is needed)

    name:
      type: string
      description: Full or partial name of the person

    email:
      type: string
      description: Email or domain

    address:
      type: string
      description: Full or partial address

  additionalProperties: false


output_schema:

  type: object

  properties:

    success:
      type: boolean

    result:

      type: object

      nullable: true

      properties:

        match_found:
          type: boolean

        confidence:
          type: number

        person:

          type: object

          properties:

            id:
              type: string

            name:
              type: string

            company:
              type: string

            title:
              type: string

            email:
              type: string

            phone:
              type: string

            address:
              type: string

            linkedin:
              type: string

            industry:
              type: string