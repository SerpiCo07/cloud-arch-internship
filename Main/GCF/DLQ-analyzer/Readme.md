This is a documention for python script which is in charge of pulling failed messages from DLQ-sub not only ask for their retrasmissions but also analyze them right now I don't know exacly what it must do just I know logging and categorizing the failed messages should be implemented on it


### What should it do ?

It  should be triggered by new event in DLQ-sub
what is it supposed to receive :
    A message that contains the address of the required file in the storage
    