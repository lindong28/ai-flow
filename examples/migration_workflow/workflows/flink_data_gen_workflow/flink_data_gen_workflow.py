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
#
import ai_flow as af
from ai_flow_plugins.job_plugins.flink import FlinkJavaProcessor


def main():
    af.init_ai_flow_context()
    af.current_project_context().get_jar_dependencies_path()
    with af.job_config('data_produce'):
        af.user_define_operation(processor=FlinkJavaProcessor(entry_class="org.ai_flow.HourlyDataPartitionJob",
                                                              main_jar_file="../../dependencies/jar/aiflow_commit_policy-1.0-SNAPSHOT.jar",
                                                              args=["kafka-kafka-bootstrap.kafka:9092", "mnist-train", "hdfs://hadoop-hdfs-namenodes.hadoop:8020/usr/flink/mnist_daily"]))

    workflow_name = af.current_workflow_config().workflow_name
    af.workflow_operation.submit_workflow(workflow_name)
    af.workflow_operation.start_new_workflow_execution(workflow_name)


if __name__ == '__main__':
    main()
