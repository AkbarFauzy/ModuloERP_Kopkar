import frappe
import json

@frappe.whitelist()
def get_stnk():
    try:
        data = frappe.get_all("STNK", fields=["*"])
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
def get_stnk_by_id(docname):
    try:
        if not frappe.has_permission("STNK", "read", doc=docname):
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
        data = frappe.get_all("STNK", fields=["*"], filters=[["description", "like", "%Pembelian%"]])
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
def get_penjualan_stnk():
    try:
        data = frappe.get_all("STNK", fields=["*"], filters=[["description", "like", "%Penjualan%"]])
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
def add_stnk(
    reference_number,
    customer_name,
    salesman_name,
    warehouse_name,
    departement_name,
    transaction_date,
    required_by,
    bank_account,
    no_document,
    note_detail,
    currency,
    exchange_rate,
    description,
    account_code,
    price,
    qty,
    discount,
    other_fee,
    final_discount,
    is_tunai
):
    try:
        if not frappe.has_permission("STNK", "create"):
            frappe.throw(("Not permitted"), frappe.PermissionError)

        new_record = frappe.get_doc({
            "doctype": "STNK",
            "reference_number": reference_number,
            "customer_name": customer_name,
            "salesman_name": salesman_name,
            "warehouse_name": warehouse_name,
            "departement_name": departement_name,
            "transaction_date": transaction_date,
            "required_by": required_by,
            "bank_account": bank_account,
            "no_document": no_document,
            "note_detail": note_detail,
            "currency": currency,
            "exchange_rate": exchange_rate,
            "description": description,
            "account_code": account_code,
            "price": price,
            "qty": qty,
            "discount": discount,
            "other_fee": other_fee,
            "final_discount": final_discount,
            "is_tunai": is_tunai
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
def update_stnk(docname, updates):
    try:
        if not frappe.has_permission("STNK", "write"):
            frappe.throw(("Not permitted"), frappe.PermissionError)

        doc = frappe.get_doc("STNK", docname)

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
            "message": f"STNK {docname} does not exist"
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
def delete_stnk(docname):
    try:
        if not frappe.has_permission("STNK", "delete"):
            frappe.throw(("Not permitted"), frappe.PermissionError)

        doc = frappe.get_doc("STNK", docname)

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
