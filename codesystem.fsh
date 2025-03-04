CodeSystem: SimpleExampleCS
Id: simple-example-cs
Title: "Simple Example CodeSystem"
Description: "A simple example CodeSystem in FSH format."
* ^status: #active
* ^content: #complete
* ^url: "http://example.org/fhir/CodeSystem/simple-example-cs"
* ^version: "1.0.0"
* ^property[0].code = #foo
* ^property[=].description = "A boolean property example"
* ^property[=].type = #boolean
* ^property[+].code = #normalizedCode
* ^property[=].description = "A code property example"
* ^property[=].type = #code
* #code1 "First Code" "Description for the first code"
* #code1 ^designation[0].value = "NOT Segundo Código"
* #code1 ^designation[=].language = "es"
* #code1 ^designation[=].use = #display
* #code1 ^designation[+].value = "LE Segundo Código"
* #code1 ^designation[=].language = "fr"
* #code1 ^designation[=].use = http://fnorb#display
* #code1 ^property[0].code = normalizedCode
* #code1 ^property[=].valueCode = #C001
* #code1 ^property[+].code = foo
* #code1 ^property[=].valueBoolean = true
* #code1 ^property[+].code = bar
* #code1 ^property[=].valueString = "hhgjkdfhgkfd"
* #code2 "Second Code" "Description for the second code"
* #code2 ^property[0].code = "myProp"
* #code2 ^property[=].valueString = "my value"
* #code3 "Third Code" "Description for the third code"
