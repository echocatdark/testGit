#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""
This is only an example DAG to highlight usage of AzureCosmosDocumentSensor to detect
if a document now exists.

You can trigger this manually with `airflow dags trigger example_cosmosdb_sensor`.

*Note: Make sure that connection `azure_cosmos_default` is properly set before running
this example.*
"""

from airflow import DAG
from airflow.providers.microsoft.azure.operators.azure_cosmos import AzureCosmosInsertDocumentOperator
from airflow.providers.microsoft.azure.sensors.azure_cosmos import AzureCosmosDocumentSensor
from airflow.utils import dates

with DAG(
    dag_id='example_azure_cosmosdb_sensor',
    default_args={
        'owner': 'airflow',
        'depends_on_past': False,
        'email': ['airflow@example.com'],
        'email_on_failure': False,
        'email_on_retry': False,
    },
    start_date=dates.days_ago(2),
    doc_md=__doc__,
    tags=['example'],
) as dag:

    t1 = AzureCosmosDocumentSensor(
        task_id='check_cosmos_file',
        database_name='airflow_example_db',
        collection_name='airflow_example_coll',
        document_id='airflow_checkid',
        azure_cosmos_conn_id='azure_cosmos_default',
    )

    t2 = AzureCosmosInsertDocumentOperator(
        task_id='insert_cosmos_file',
        database_name='airflow_example_db',
        collection_name='new-collection',
        document={"id": "someuniqueid", "param1": "value1", "param2": "value2"},
        azure_cosmos_conn_id='azure_cosmos_default',
    )

    t1 >> t2
