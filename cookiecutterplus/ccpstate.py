import argparse

class CCPStateManager:
    def __init__(self):
        self.metadata = {
            'api_mode': {
                'flags': ['-a', '--api-mode'],
                'type': bool,
                'help': 'Run CookieCutterPlus in API Mode',
                'required': False,
                'default': False
            },
            'template_repo': {
                'flags': ['-t', '--template_repo'],
                'type': str,
                'help': 'The template repo to use',
                'required': True,
                'default': None
            },
            'payload': {
                'flags': ['-p', '--payload'],
                'type': dict,
                'help': 'The payload to use',
                'required': True,
                'default': None
            },
            'output_path': {
                'flags': ['-o', '--output_path'],
                'type': str,
                'help': 'The output path to use',
                'required': True,
                'default': None
            },
            'no_input': {
                'flags': ['-n', '--no_input'],
                'type': bool,
                'help': 'If enabled, you will be prompted for variable input.',
                'required': False,
                'default': True
            }
        }

    def parse_args(self, args):
        parser = argparse.ArgumentParser(description='CookiecutterPlus CLI')
        for arg, metadata in self.metadata.items():
            parser.add_argument(*metadata['flags'],
                                type=metadata['type'],
                                help=metadata['help'],
                                default=metadata['default'])
        parsed = vars(parser.parse_args(args))
        print(f"parsed args {parsed}")
        return self.validate_args(parsed)

    def validate_args(self, args):
        if args.get('api_mode', None) is None:
            missing_requirements = []
            for name, meta in self.metadata.items():
                if meta.get('required') and args.get(name, None) is None:
                    missing_requirements.append(name)
                if meta.get('default') and args.get(name, None) is None:
                    args[name] = meta.get('default')

            if len(missing_requirements) > 0:
                raise ValueError(f'Missing required attributes: {missing_requirements}')

        return args
