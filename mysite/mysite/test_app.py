#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 31/3/19 3:58 PM
# @Author  : zchai
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def search_post(request):
    ctx ={}
    if request.POST:
        ctx['rlt'] = request.POST['sentence']
        print(ctx)
    return HttpResponse('success')