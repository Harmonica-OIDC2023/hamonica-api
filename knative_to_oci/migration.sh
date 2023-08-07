source .env

fn init --runtime python \
        --entrypoint "/python/bin/fdk /function/func.py main" \
        $FUNCTION_NAME

python3 migration.py

mv ./func.py $FUNCTION_NAME/func.py
mv ./requirements.txt $FUNCTION_NAME/requirements.txt

oci fn application create -c $COMPARTMENT_ID \
                        --display-name $FNAPP_NAME \
                        --subnet-ids '["'"${SUBNET_ID}"'"]'

fn deploy --working-dir /app/oci_to_knative/$FUNCTION_NAME --app $FNAPP_NAME