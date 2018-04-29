import json
from django.http import Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Category


@csrf_exempt
def add_new_categories(request):
    def validate(data):
        print('Check {}'.format(data['name']))
        if not isinstance(data, dict):
            raise Exception('Category must be a dictionary')
        if 'name' not in data:
            raise Exception('Category must have a name field')
        if not isinstance(data['name'], str):
            raise Exception('Name must be a string')
        names = [data['name']]
        if 'children' in data:
            for child in data['children']:
                children_names = validate(child)
                print(children_names)
                # Check for name duplicates
                for child_name in children_names:
                    if child_name in names:
                        raise Exception('Name must be unique, there is duplicate for <{}>'.format(child_name))
                    names.append(child_name)
        return names


    if request.method != 'POST':
        raise Http404('Page not found')

    response = {}
    errors = []

    try:
        data = json.loads(request.body.decode('utf-8'))
        validate(data)
        response['rows_processed'] = Category.add_new_category(**data)
    except json.decoder.JSONDecodeError:
        errors.append('Json is not valid')
    except Exception as e:
        errors.append(str(e))

    if len(errors):
        response['errors'] = errors

    return JsonResponse(response)
