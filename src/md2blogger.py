import argparse
from pyspark_app.feature_generators.factory import FeatureGeneratorFactory

from pyspark_app.feature_generators.gfa import *
from pyspark_app.feature_generators.ncc import *
from pyspark_app.feature_generators.ncc.rsa import *
from pyspark_app.feature_generators.search import *


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--job_name", required=True)
    parser.add_argument("--ymd", required=True)
    parser.add_argument("--hms", required=True)
    parser.add_argument("--env", required=True)
    parser.add_argument("--version", required=False, default="")
    parser.add_argument(
        "--optional_params",
        required=False,
        type=str,
        help="""추가적으로 입력하고 싶은 params를 json 형태로 입력합니다. Ex) '{"key1":"value1","key2":"value2"}'""",
        default="{}",
    )

    args = parser.parse_args()
    feature_generator = FeatureGeneratorFactory.create_feature_generator(args.job_name, args)
    feature_generator.run()



import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--job_name", required=True)
    parser.add_argument("--ymd", required=True)
    parser.add_argument("--hms", required=True)
    parser.add_argument("--env", required=True)
    parser.add_argument("--version", required=False, default="")
    parser.add_argument(
        "--optional_params",
        required=False,
        type=str,
        help="""추가적으로 입력하고 싶은 params를 json 형태로 입력합니다. Ex) '{"key1":"value1","key2":"value2"}'""",
        default="{}",
    )

    args = parser.parse_args()
    feature_generator = FeatureGeneratorFactory.create_feature_generator(args.job_name, args)
    feature_generator.run()