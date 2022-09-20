### query
def dispatch(self, *args, **kwargs):
        response = super().dispatch(*args, **kwargs)
        # For debugging purposes only.
        from django.db import connection
        #print(connection.queries)
        #print('# of Queries: {}'.format(len(connection.queries)))
        return response

def dictfetchall(cursor,data):
    columns = [col[0] for col in cursor.description]
    result = list()
    for row in data:
        result.append(dict(zip(columns, row)))
    return result

def dictfetchone(cursor,data):
    columns = [col[0] for col in cursor.description]
    result = dict(zip(columns, data))
    return result 

def dict_detail_reservation(cursor,data):
    results = list()
    columns = [col[0] for col in cursor.description]    
    for row in data:
       results.append(dict(zip(columns, row)))

    rooms = [  results[i]['tipo_habitacion']  for i in range(0,len( results))]
    quantity = [  results[i]['cantidad_habitacion']  for i in range(0,len( results))]
    type_rooms = dict(zip(rooms, quantity))
    result = results[0]
    result['tipos_habitacion'] = type_rooms
    return result

def dict_rooms_availability(cursor,data):
    columns = [col[0] for col in cursor.description]
    result = list()
    for row in data:        
        result.append(dict(zip(columns, row)))

    rooms_available =  { row['tipo_habitacion']: row['cantidad_habitacion']  for row in result }
    
    return rooms_available



def dict_rooms(data,rooms):
    obj = { j : []  for j in rooms }

    for t  in data:
     obj[t['habitacion']]= t['registros']  
    
    return obj
























#--------------------------
def dict_detail_reservation2(cursor,data):
    results = list()
    columns = [col[0] for col in cursor.description]    
    for row in data:
       results.append(dict(zip(columns, row)))

    rooms = [  results[i]['tipos_habitacion']  for i in range(0,len( results))]
    

    result = results[0]
    result['tipos_habitacion'] = type_rooms
    return result



def dict_rooms2(data):
    tipo = list(set([ i['tipo_habitacion']  for i in data]))
    obj = { j : []  for j in tipo }

    for t  in data:
        obj[t['tipo_habitacion']].append(t)  
    
    return obj

'''         
    try:            
        with connection.cursor() as cursor:
        cursor.callproc('fn_buscarcliente',[hotel_id,numero_documento])
        data = cursor.fetchone() 
            if data :
                result = dictfetchone(cursor,data) 
                return JsonResponse(result)                   
                return Response({}, status=status.HTTP_200_OK)                    
     except Exception as e:
       return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
 '''
