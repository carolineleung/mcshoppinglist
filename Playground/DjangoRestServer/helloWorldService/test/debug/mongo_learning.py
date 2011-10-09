from mongoengine import *
connect('test')


class OrangeDoc(Document):
    data = StringField()

print 'Count before drop: {0}'.format(OrangeDoc.objects.count())
js_code = """
db.dropDatabase();
"""
OrangeDoc.objects.exec_js(js_code)
print 'Count after drop: {0}'.format(OrangeDoc.objects.count())

doc1 = OrangeDoc(data='data1')
doc1.save()
doc1_id_str = str(doc1.id)
print 'ObjectId = {0}'.format(doc1_id_str)

doc1_retrieved = OrangeDoc.objects.get(id=doc1_id_str)
print 'Got:\n{0}'.format(doc1_retrieved)
print 'Data:\n{0}'.format(doc1_retrieved.data)
