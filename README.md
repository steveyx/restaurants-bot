installation: 
   pip install -r requirements.txt

Commands:
*  train chatbot in terminal
       rasa train
       
*  to run chatbot with rasa-x (web, local model)
       rasa x
       rasa run actions
   
*  to run chatbot in terminal and run action server
       rasa shell --debug
       rasa run actions
 
-  open a new terminal and run action server (for debug mode -vv)
       rasa run actions
       
-  to run rasa shell with debug mode
       rasa shell --debug