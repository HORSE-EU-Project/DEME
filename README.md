# DEME-apis
## Paths

### GET */detection*

#### Summary
Atk Detection


#### Description
Returns the estimate for the last POST /estimate processed on the system.
The estimate refers to each instance of the network and contains the type of attack identified and the accuracy of the prediction.

Returns:
- A list of Detection objects.


#### Responses


200 OK
TODO

### GET */dump_configuration*

#### Summary
Dump Configuration


#### Description
Retrieves network and features information.

Returns:
- A list of Configuration objects.


#### Responses


200 OK
TODO

### POST */estimate*

#### Summary
Atk Estimate


#### Description
Estimates, for each network instance, the presence of a possible attack using a 2-stage machine learning chain
starting from its network state of a specific instant.

Request Body:
- A list of Estimate object

Returns:
- JSON response DoneResponse.


#### Responses


200 OK
TODO
422 Unprocessable Entity
TODO

### GET */is_ok*

#### Summary
Atk Ok


#### Description
This endpoint verifies Analytic Toolkit is up and running.

Returns:
- JSON response IsOK.


#### Responses


200 OK
TODO

### GET */is_ready*

#### Summary
Atk Ready


#### Description
This endpoint verifies Analytic Toolkit is ready.

Returns:
- JSON response TrueResponse.


#### Responses


200 OK
TODO


