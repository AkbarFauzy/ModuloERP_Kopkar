import frappe
import json

@frappe.whitelist()
# def get_penjualan_stnk():
#     try:
#         data = frappe.get_all("Penjualan STNK", fields=[
#                 'customer_name',
#                 'invoice_number',
#                 'so_number',
#                 'invoice_date',
#                 'delivery_date',
#                 'project',
#                 'department',
#                 'description',
#                 'description_note',
#                 'code',
#                 'salesman',
#                 'qty',
#                 'price',
#                 'discount',
#                 'tax',
#                 'job',
#                 'other_fee',
#                 'is_tunai',
#                 'payment_term',
#                 'crede_card',
#                 'tax_total',
#                 'total_after_tax',
#                 'down_payment',
#                 'balance',
#         ])
#         response = {
#             "status": 200,
#             "message": "success",
#             "data": data,
#         }

#     except frappe.PermissionError:
#         return {
#             "status": 500,
#             "message": "Internal Server Error"
#         }

#     except Exception as e:
#         return {
#             "status": 500,
#             "message": "Internal Server Error"
#         }

#     return response

@frappe.whitelist()
def get_penjualan_stnk_by_id(docname):
    try:
        if not frappe.has_permission("Penjualan STNK", "read", doc=docname):
            frappe.throw(("Not permitted"), frappe.PermissionError)

        doc = frappe.get_doc("Penjualan STNK", docname)

        # serialized_doc = frappe.as_json(doc.as_dict())

        response = {
            "status": 200,
            "message": "success",
            "data": doc,
        }
    except frappe.PermissionError:
        return {
            "status": 500,
            "message": "Internal Server Error"
        }

    except Exception as e:
        return {
            "status": 500,
            "message": "Internal Server Error"
        }

    return response

@frappe.whitelist()
def get_penjualan_stnk():
    try:
        data = frappe.get_all("Penjualan STNK", fields=["*"])
        response = {
            "status": 200,
            "message": "success",
            "data": data,
        }
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), ("STNK API Error"))
        response = {
            "status": 500,
            "message": "Internal Server Error"
        }

    return response

@frappe.whitelist()
def add_penjualan_stnk(
    customer_name,
    invoice_number,
    so_number,
    invoice_date,
    delivery_date,
    project,
    department,
    description,
    description_note,
    code,
    salesman,
    qty,
    price,
    discount,
    tax,
    job,
    other_fee,
    payment_term,
    crede_card,
    is_tunai,
    tax_total,
    total_after_tax,
    down_payment,
    balance
):
    try:
        if not frappe.has_permission("Penjualan STNK", "create"):
            frappe.throw(("Not permitted"), frappe.PermissionError)

        new_record = frappe.get_doc({
            "doctype": "Penjualan STNK",
            "customer_name": customer_name,
            "invoice_number": invoice_number,
            "so_number": so_number,
            "invoice_date": invoice_date,
            "delivery_date": delivery_date,
            "project": project,
            "department": department,
            "description": description,
            "description_note": description_note,
            "code": code,
            "salesman": salesman,
            "qty": qty,
            "price": price,
            "discount": discount,
            "tax": tax,
            "job": job,
            "other_fee": other_fee,
            "payment_term": payment_term,
            "crede_card": crede_card,
            "is_tunai": is_tunai,
            "tax_total" : tax_total,
            "total_after_tax": total_after_tax,
            "down_payment": down_payment,
            "balance":balance,
        })

        new_record.insert()

        response = {
            "status": 200,
            "message": "success",
            "data": new_record
        }

    except Exception as e:

        frappe.log_error(frappe.get_traceback(), ("STNK API Error"))
        response = {
            "status": 500,
            "message": "Internal Server Error",
        }

    return response

@frappe.whitelist()
def update_penjualan_stnk():
    try:
        data = frappe.request.json
        if not frappe.has_permission("Penjualan STNK", "write"):
            frappe.throw(("Not permitted"), frappe.PermissionError)

        docname = data.get('docname')
        updates = data.get('updates') 

        doc = frappe.get_doc("Penjualan STNK", docname)

        for field, value in updates.items():
            if hasattr(doc, field):
                setattr(doc, field, value)
            else:
                return {
                    "status": 400,
                    "message": f"Field '{field}' either does not exist or cannot be modified"
                }

        doc.save()

        return {
            "status": 200,
            "message": "success",
            "data": doc
        }

    except frappe.DoesNotExistError:
        return {
            "status": 500,
            "message": f"Penjualan STNK {docname} does not exist"
        }

    except frappe.PermissionError:
        return {
            "status": 500,
            "message": "You don't have permission to update this document"
        }

    except Exception as e:
        return {
            "status": 500,
            "message": "Internal Server Error",
            "e":e
        }


@frappe.whitelist()
def delete_penjualan_stnk(docname):
    try:
        if not frappe.has_permission("Penjualan STNK", "delete"):
            frappe.throw(("Not permitted"), frappe.PermissionError)

        doc = frappe.get_doc("Penjualan STNK", docname)

        doc.delete()

        return {
            "status": 200,
            "message": "success"
        }

    except frappe.DoesNotExistError:
        return {
            "status": 500,
            "message": f"STNK {docname} does not exist"
        }

    except frappe.PermissionError:
        return {
            "status": 500,
            "message": "You don't have permission to delete this document"
        }

    except Exception as e:
        return {
            "status": 500,
            "message": "Internal Server Error"
        }
