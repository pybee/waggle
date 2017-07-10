import os
import re
import subprocess
import sys

from botocore.exceptions import ClientError
import boto3

from argparse import ArgumentParser


def register(options):
    bad_names = []
    not_a_dir = []
    tasks = []
    for dirname in options.dirnames:
        full_path = os.path.abspath(dirname)
        task_name = os.path.basename(full_path)
        if re.match('[^-_A-Za-z0-9]', task_name):
            bad_names.append(task_name)
        elif not os.path.isdir(full_path):
            not_a_dir.append(task_name)
        else:
            tasks.append((task_name, full_path))

    if bad_names:
        print()
        print("The following tasks will not be valid ECS tasks:")
        for name in bad_names:
            print("    *", name)

    if not_a_dir:
        print()
        print("The following paths don't appear to be Docker configurations:")
        for name in not_a_dir:
            print("    *", name)

    if bad_names or not_a_dir:
        return

    print("Logging into ECR...")
    result = subprocess.run([
            'aws', 'ecr', 'get-login',
            '--no-include-email',
            '--region', options.AWS_ECS_REGION_NAME
        ],
        stdout=subprocess.PIPE
    )
    subprocess.run(result.stdout.decode('utf-8').strip().split(' '),
        cwd=full_path,
        check=True
    )

    registered = []
    for task_name, full_path in tasks:
        _register(task_name, full_path, options)
        registered.append(task_name)

    print()
    print("The following tasks have been registered with AWS ECS:")
    for task in registered:
        print('    * %s' % task)


def _register(task_name, full_path, options):
    try:
        repository_name = "%s/%s" % (
            options.namespace,
            task_name
        )
        print("Registering %s as an AWS ECS task..." % repository_name)
        print("Building local Docker image for %s..." % repository_name)
        subprocess.run([
                'docker', 'build',
                "-t", repository_name,
                '.'
            ],
            cwd=full_path,
            check=True
        )

        print("Looking up AWS ECR repository URI...")
        aws_session = boto3.session.Session(
            region_name=options.AWS_ECS_REGION_NAME,
            aws_access_key_id=options.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=options.AWS_SECRET_ACCESS_KEY,
        )
        ecr = aws_session.client('ecr')
        try:
            response = ecr.describe_repositories(repositoryNames=[repository_name])
            uri = response['repositories'][0]['repositoryUri']
        except ClientError as e:
            response = ecr.create_repository(repositoryName=repository_name)
            uri = response['repository']['repositoryUri']
        print("   ECR repository URI is", uri)

        print("Tagging Docker image for publication...")
        subprocess.run([
                'docker', 'tag',
                "%s:%s" % (repository_name, options.tag),
                "%s:%s" % (uri, options.tag),
            ],
            cwd=full_path,
            check=True
        )

        print("Pushing Docker image to AWS...")
        subprocess.run([
                'docker', 'push',
                "%s:%s" % (uri, options.tag),
            ],
            cwd=full_path,
            check=True
        )

        print("Registering ECS task...")
        definition = {
            'name': task_name,
            'image': uri,
            'memory': 128,
            'cpu': 0,
            'logConfiguration': {
                'logDriver': 'awslogs',
                'options': {
                    'awslogs-group': options.namespace,
                    'awslogs-region': options.AWS_ECS_REGION_NAME,
                    'awslogs-stream-prefix': task_name
                }
            }
        }

        try:
            with open(os.path.join(full_path, 'ecs.json')) as data:
                definition.update(json.load(data))
        except IOError:
            print("Couldn't load ecs.json configuration; using defaults")

        ecs = aws_session.client('ecs')
        response = ecs.register_task_definition(
            family=task_name,
            networkMode='bridge',
            containerDefinitions=[definition]
        )

        revision = response['taskDefinition']['revision']

        print("AWS ECS task registration complete.")

        return "%s:%s" % (task_name, revision)

    except Exception as e:
        print("Unable to prepare AWS task %s" % full_path)
        print(e)


def main():
    parser = ArgumentParser()
    parser.add_argument(
        '--tag', '-t', default='latest', dest='tag',
        help='Specify the version tag to use.',
    )
    parser.add_argument(
        '--namespace', default='beekeeper', dest='namespace',
        help='Specify the namespace to use for AWS services.',
    )
    parser.add_argument('dirnames', metavar='dirname', nargs='+', help='Docker image directories to register.')
    options = parser.parse_args()

    # Load sensitive environment variables from a .env file
    try:
        with open('.env') as envfile:
            for line in envfile:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ.setdefault(key.strip(), value.strip())
    except FileNotFoundError:
        pass

    try:
        options.AWS_ECS_REGION_NAME = os.environ['AWS_ECS_REGION_NAME']
        options.AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
        options.AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    except KeyError as e:
        print("AWS environment variable %s not found" % e)
        sys.exit(1)

    register(options)


if __name__ == '__main__':
    main()
