CodeSystem: SimpleExampleCS
Id: simple-example-cs
Title: "Simple Example CodeSystem"
Description: "A simple example CodeSystem in FSH format."
* ^content: #complete
* ^status: #active
* ^url: "http://example.org/fhir/CodeSystem/simple-example-cs"
* ^version: "1.0.0"
* ^property[0].code = #foo
* ^property[=].description = "A boolean property example"
* ^property[=].type = #boolean
* ^property[+].code = #normalizedCode
* ^property[=].description = "A code property example"
* ^property[=].type = #code

* #code1 "First Code" "Description for the first code"
* #code1 ^property[0].code = #bar
* #code1 ^property[=].valueString = "hhgjkdfhgkfd"
* #code1 ^property[+].code = #foo
* #code1 ^property[=].valueBoolean = true
* #code1 ^property[+].code = #inactive
* #code1 ^property[=].valueString = "true"
* #code1 ^property[+].code = #ormalizedCode
* #code1 ^property[=].valueString = "C001"
* #code1 ^designation[0].value = "NOT Segundo Código"
* #code1 ^designation[=].language = "es"
* #code1 ^designation[=].use = #display
* #code1 ^designation[+].value = "LE Segundo Código"
* #code1 ^designation[=].language = "fr"
* #code1 ^designation[=].use = http://fnorb#display
* #code2 "Second Code" "Description for the second code"
* #code2 ^property[0].code = #category
* #code2 ^property[=].valueString = "Category B"
* #code2 ^property[+].code = #normalizedCode
* #code2 ^property[=].valueCode = #C002
* #code2 ^designation[0].value = "Segundo Código"
* #code2 ^designation[=].language = "es"
* #code2 ^designation[=].use = #display
* #code3 "Third Code" "Description for the third code"
* #code3 ^property[0].code = #category
* #code3 ^property[=].valueString = "Category A"
* #code3 ^property[+].code = #normalizedCode
* #code3 ^property[=].valueCode = #C003
* #code3 ^designation[0].value = "Tercer Código"
* #code3 ^designation[=].language = "es"
* #code3 ^designation[=].use = #display
* #code4 "First Code" "Description for the first code"
* #code4 ^property[0].code = #category
* #code4 ^property[=].valueString = "Category A"
* #code4 ^property[+].code = #normalizedCode
* #code4 ^property[=].valueCode = #C001
* #code4 ^designation[0].value = "Primer Código"
* #code4 ^designation[=].language = "es"
* #code4 ^designation[=].use = #display
* #code4 ^designation[+].value = "Initio Codio"
* #code4 ^designation[=].language = "es"
* #code4 ^designation[=].use = #display
