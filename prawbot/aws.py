from app import session
import json

def add_rules_for_subs():
    event_client = session.client('events')

    subreddits = [
        'MadeMeSmile',
        'Home',
        'formula1',
        'CasualUK',
        'OnePiece',
        'WhitePeopleTwitter',
        'entertainment',
        'interestingasfuck',
        'mildlyinteresting',
        'pics',
        'MapPorn',
        'pcmasterrace',
        'HolUp',
        'ukraine',
        'Genshin_Impact',
        'leagueoflegends',
        'memes',
        'worldnews',
        'gaming',
        'nextfuckinglevel',
        'terriblefacebookmemes',
        'AmItheAsshole',
        'mildlyinfuriating',
        'Whatcouldgowrong',
        'NoStupidQuestions',
        'explainlikeimfive',
        'Tinder',
        'Eldenring',
        'BlackPeopleTwitter',
        'betterCallSaul',
        'BestofRedditorUpdates',
        'LivestreamFail',
        'Minecraft',
        'AskReddit',
        'tifu',
        'PublicFreakout',
        'antiwork',
        'politics',
        'JusticeServed',
        'facepalm',
        'Unexpected',
        'news',
        'todayilearned',
        'Damnthatsinteresting',
        'movies',
        'funny',
        'TwoXChromosomes',
        'ProgrammerHumor',
        'wallstreetbets',
    ]
    hour = 10
    for sub in subreddits:

        hour += 1
        if hour == 22:
            hour=10

        rule_name = f'run-{sub}' # Define a var for rule_name
        cron_sec = f'cron(0 {hour} * * ? *)' # Define a var for cron
        lambda_fc_name = 'run-praw-scrape' # Define a var for lambda name
        lambda_fc_arn = 'arn:aws:lambda:us-east-1:879546063241:function:run-praw-scrape' # Here you need copy the lambda_fc_name function arn
        add_permission_role_arn = 'arn:aws:iam::879546063241:role/CloudwatchEventRole' # put create role ARN
        # use boto3 create a rule
        create_rule_resp = event_client.put_rule(
            Name=rule_name, # There put your rule name
            ScheduleExpression=cron_sec, # there put your cron
            State='ENABLED', # there set the rule state ENABLED or DISABLED
            EventBusName='default', # set eventbus ,I use default
            RoleArn=add_permission_role_arn,
            Description=f'Run @ {hour-4} est'
        )

        put_target_resp = event_client.put_targets(
            Rule=rule_name,
            Targets=[{
                'Id': lambda_fc_name,
                'Arn': lambda_fc_arn,
                'Input': json.dumps(
                    {
                        "detail": {
                            "subreddit": sub
                        }
                    }
                )
            }]
        )

if __name__=='__main__':
    add_rules_for_subs()