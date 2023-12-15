import frappe
import json

@frappe.whitelist()
def get_pembelian_stnk():
    try:
        frappe.db.get_list('Pembelian STNK',
            fields=[
                'supplier_name',
                'purchase_number',
                'po_number',
                'invoice_date',
                'delivery_date',
                'project',
                'department',
                'description',
                'description_note',
                'code',
                'purchase_bag',
                'qty',
                'price',
                'discount',
                'tax',
                'job',
                'other_fee',
                'is_tunai',
                'tax_total',
                'total_after_tax',
                'down_payment',
                'balance',
                ],
            order_by='date desc',
            start=10,
            page_length=20,
            as_list=True
        )

        response = {
            "status": 200,
            "message": "success",
            "data": data,
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
def get_pembelian_stnk_by_id(docname):
    try:
        if not frappe.has_permission("Pembelian STNK", "read", doc=docname):
            frappe.throw(("Not permitted"), frappe.PermissionError)

        doc = frappe.get_doc("STNK", docname)

        serialized_doc = frappe.as_json(doc.as_dict())

        response = {
            "status": 200,
            "message": "success",
            "data": serialized_doc,
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
def get_pembelian_stnk():
    try:
        data = frappe.get_all("Pembelian STNK", fields=["*"])
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
def add_pembelian_stnk(
    supplier_name,
    purchase_number,
    po_number,
    invoice_date,
    delivery_date,
    project,
    department,
    description,
    description_note,
    code,
    purchase_bag,
    qty,
    price,
    discount,
    tax,
    job,
    other_fee,
    is_tunai,
    tax_total,
    total_after_tax,
    down_payment,
    balance,
):
    try:
        if not frappe.has_permission("Pembelian STNK", "create"):
            frappe.throw(("Not permitted"), frappe.PermissionError)

        new_record = frappe.get_doc({
            "doctype": "Pembelian STNK",
            "supplier_name": supplier_name,
            "purchase_number": purchase_number,
            "po_number": po_number,
            "invoice_date": invoice_date,
            "delivery_date": delivery_date,
            "project": project,
            "department": department,
            "description": description,
            "description_note": description_note,
            "code": code,
            "purchase_bag": purchase_bag,
            "qty": qty,
            "price": price,
            "discount": discount,
            "tax": tax,
            "job": job,
            "other_fee": other_fee,
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
def update_pembelian_stnk(docname, updates):
    try:
        if not frappe.has_permission("Pembelian STNK", "write"):
            frappe.throw(("Not permitted"), frappe.PermissionError)

        doc = frappe.get_doc("Pembelian STNK", docname)

        for field, value in updates.items():
            if hasattr(doc, field):
                setattr(doc, field, value)

        doc.save()

        return {
            "status": 200,
            "message": "success"
        }

    except frappe.DoesNotExistError:
        return {
            "status": 500,
            "message": f"Pembelian STNK {docname} does not exist"
        }

    except frappe.PermissionError:
        return {
            "status": 500,
            "message": "You don't have permission to update this document"
        }

    except Exception as e:
        return {
            "status": 500,
            "message": "Internal Server Error"
        }


@frappe.whitelist()
def delete_pembelian_stnk(docname):
    try:
        if not frappe.has_permission("pembelian STNK", "delete"):
            frappe.throw(("Not permitted"), frappe.PermissionError)

        doc = frappe.get_doc("pembelian STNK", docname)

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
