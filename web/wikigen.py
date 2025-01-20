import argparse
import logging
import sys

from scripts.builder import WikiBuilder, WikiBuilderError

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command',
        help='Command to run (build | clear)'
    )
    parser.add_argument('-log', '--loglevel',
        default='info',
        help='Logging level. Example --loglevel debug, default=info'
    )
    args = parser.parse_args()

    logging.basicConfig(level=args.loglevel.upper())
    logger = logging.getLogger('wikigen')
    
    try:
        wb = WikiBuilder(logger)

        if args.command == 'build':
            wb.build()
        elif args.command == 'clear':
            wb.clear()
        else:
            logger.error('Unknown command: %s', args.command)
            sys.exit(1)
    except KeyboardInterrupt:
        logger.info('Cancelled by user input...')
        sys.exit(0)
    except WikiBuilderError as e:
        logger.error('Error occurred during build process...')
        logger.error(e)
        sys.exit(1)
    except Exception as e:
        logger.exception(e)
        sys.exit(1)

if __name__ == '__main__':
    main()