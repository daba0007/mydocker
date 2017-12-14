 #!/bin/bash
#
cd mysql                                                                                                            
echo "start mysql----------------"
sh start.sh

cd ../redis  
echo "start redis---------------------"
sh start.sh

cd ../web 
echo "start web ---------------------"
sh start.sh

cd ../nginx
echo "start nginx-------------------"
sh start.sh
