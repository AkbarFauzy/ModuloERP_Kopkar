import frappe

@frappe.whitelist()
def get_purchase_invoice():
    try:
        main_data = frappe.get_all('Purchase Invoice', fields=["*"])
        for entry in main_data:
            entry['items'] = frappe.get_all('Purchase Invoice Item', 
                                            filters={'parent': entry['name']},
                                            fields=["*"])

        response = {
            "status": 200,
            "message": "success",
            "data": main_data,
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), ("Purchase Invoice"))
        response = {
            "status": 500,
            "message": "Internal Server Error"
        }

    return response

@frappe.whitelist()
def get_purchase_invoice_by_id(docname):
    try:
        if not frappe.has_permission("Purchase Invoice", "read", doc=docname):
            frappe.throw(("Not permitted"), frappe.PermissionError)
        doc = frappe.get_doc("Purchase Invoice", docname)
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
def add_purchase_invoice():
    try:
        if not frappe.has_permission("Purchase Invoice", "create"):
            frappe.throw(("Not permitted"), frappe.PermissionError)

        request_data = frappe.request.json
        new_invoice = frappe.new_doc('Purchase Invoice')
        for field, value in request_data.items():
            if field == 'items':
                continue  # Skip 'items' field, handle it separately
            if hasattr(new_invoice, field):
                setattr(new_invoice, field, value)
            else:
                return field

        items_data = request_data.get('items', [])
        if items_data:  # Check if items_data is not empty
            for item_data in items_data:
                new_item = new_invoice.append('items', {})
                for field, value in item_data.items():
                    setattr(new_item, field, value)

        new_invoice.insert()
        new_invoice.save()  # Save the Purchase Invoice with items

        frappe.db.commit()

        new_invoice.submit()

        return {
            'status': 200,
            'message': 'Purchase Invoice created successfully',
            'docname': new_invoice
        }

    except Exception as e:
        return {
            "status": 500,
            "message": "Internal Server Error",
            "e":e
        }


@frappe.whitelist()
def update_purchase_invoice():
    try:
        data = frappe.request.json
        if not frappe.has_permission("Purchase Invoice", "write"):
            frappe.throw(("Not permitted"), frappe.PermissionError)

        docname = data.get('docname')
        updates = data.get('updates')

        doc = frappe.get_doc("Purchase Invoice", docname)

        for field, value in updates.items():
            if field == 'items':
                continue  # Skip 'items' field, handle it separately
            if hasattr(doc, field):
                setattr(doc, field, value)
            else:
                 return {
                    "status": 400,
                    "message": f"Field '{field}' either does not exist or cannot be modified"
                }

        items_data = updates.get('items', [])
        if items_data:  # Check if items_data is not empty
            for item_data in items_data:
                item_name = item_data.get('item_code')
                existing_item = next(
                        (item for item in doc.items if item.item_name == item_name), None
                    )
                if existing_item:
                    for key, val in item_data.items():
                            setattr(existing_item, key, val)
                else:
                    new_item = doc.append('items', {})
                    for key, val in item_data.items():
                        setattr(new_item, key, val)

        doc.save()

        return {
            "status": 200,
            "message": "success",
            "data": doc
        }

    except frappe.DoesNotExistError:
        return {
            "status": 500,
            "message": f"Purchase Invoice {docname} does not exist"
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
def delete_purchase_invoice(docname):
    try:
        if not frappe.has_permission("Purchase Invoice", "delete"):
            frappe.throw(("Not permitted"), frappe.PermissionError)

        doc = frappe.get_doc("Purchase Invoice", docname)

        doc.delete()

        return {
            "status": 200,
            "message": "success"
        }

    except frappe.DoesNotExistError:
        return {
            "status": 500,
            "message": f"Purchase Invoice {docname} does not exist"
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

@frappe.whitelist()
def get_payment_entry():
    try:
        main_data = frappe.get_all('Payment Entry', fields=["*"])
        response = {
            "status": 200,
            "message": "success",
            "data": main_data,
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), ("Payment Entry"))
        response = {
            "status": 500,
            "message": "Internal Server Error"
        }

    return response

@frappe.whitelist()
def get_payment_entry_by_id(docname):
    try:
        if not frappe.has_permission("Payment Entry", "read", doc=docname):
            frappe.throw(("Not permitted"), frappe.PermissionError)
        doc = frappe.get_doc("Payment Entry", docname)
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
def add_payment_entry():
    try:
        if not frappe.has_permission("Payment Entry", "create"):
            frappe.throw(("Not permitted"), frappe.PermissionError)

        request_data = frappe.request.json
        new_invoice = frappe.new_doc('Payment Entry')
        for field, value in request_data.items():
            if hasattr(new_invoice, field):
                setattr(new_invoice, field, value)
            else:
                return field
            
        new_invoice.insert()
        new_invoice.save()  

        frappe.db.commit()

        new_invoice.submit()

        return {
            'status': 200,
            'message': 'Payment Entry created successfully',
            'docname': new_invoice
        }

    except Exception as e:
        return {
            "status": 500,
            "message": "Internal Server Error",
            "e":e
        }

@frappe.whitelist()
def update_payment_entry():
    try:
        data = frappe.request.json
        if not frappe.has_permission("Payment Entry", "write"):
            frappe.throw(("Not permitted"), frappe.PermissionError)

        docname = data.get('docname')
        updates = data.get('updates')

        doc = frappe.get_doc("Payment Entry", docname)

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
            "message": f"Payment Entry {docname} does not exist"
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
def delete_payment_entry(docname):
    try:
        if not frappe.has_permission("Payment Entry", "delete"):
            frappe.throw(("Not permitted"), frappe.PermissionError)

        doc = frappe.get_doc("Payment Entry", docname)

        doc.delete()

        return {
            "status": 200,
            "message": "success"
        }

    except frappe.DoesNotExistError:
        return {
            "status": 500,
            "message": f"Payment Entry {docname} does not exist"
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

@frappe.whitelist()
def get_sales_invoice():
    try:
        main_data = frappe.get_all('Sales Invoice', fields=["*"])
        for entry in main_data:
            entry['items'] = frappe.get_all('Sales Invoice Item', 
                                            filters={'parent': entry['name']},
                                            fields=["*"])

        response = {
            "status": 200,
            "message": "success",
            "data": main_data,
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), ("Sales Invoice"))
        response = {
            "status": 500,
            "message": "Internal Server Error"
        }

    return response

@frappe.whitelist()
def get_sales_invoice_by_id(docname):
    try:
        if not frappe.has_permission("Sales Invoice", "read", doc=docname):
            frappe.throw(("Not permitted"), frappe.PermissionError)
        doc = frappe.get_doc("Sales Invoice", docname)
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
def add_sales_invoice():
    try:
        if not frappe.has_permission("Sales Invoice", "create"):
            frappe.throw(("Not permitted"), frappe.PermissionError)

        request_data = frappe.request.json
        new_invoice = frappe.new_doc('Sales Invoice')
        for field, value in request_data.items():
            if field == 'items':
                continue
            if hasattr(new_invoice, field):
                setattr(new_invoice, field, value)
            else:
                return field

        items_data = request_data.get('items', [])
        if items_data: 
            for item_data in items_data:
                new_item = new_invoice.append('items', {})
                for field, value in item_data.items():
                    setattr(new_item, field, value)

        new_invoice.insert()
        new_invoice.save()

        frappe.db.commit()

        new_invoice.submit()

        return {
            'status': 200,
            'message': 'Sales Invoice created successfully',
            'docname': new_invoice
        }

    except Exception as e:
        return {
            "status": 500,
            "message": "Internal Server Error",
            "e":e
        }



@frappe.whitelist()
def update_sales_invoice():
    try:
        data = frappe.request.json
        if not frappe.has_permission("Sales Invoice", "write"):
            frappe.throw(("Not permitted"), frappe.PermissionError)

        docname = data.get('docname')
        updates = data.get('updates')

        doc = frappe.get_doc("Sales Invoice", docname)

        for field, value in updates.items():
            if field == 'items':
                continue  # Skip 'items' field, handle it separately
            if hasattr(doc, field):
                setattr(doc, field, value)
            else:
                 return {
                    "status": 400,
                    "message": f"Field '{field}' either does not exist or cannot be modified"
                }

        items_data = updates.get('items', [])
        if items_data:  # Check if items_data is not empty
            for item_data in items_data:
                item_name = item_data.get('item_code')
                existing_item = next(
                        (item for item in doc.items if item.item_name == item_name), None
                    )
                if existing_item:
                    for key, val in item_data.items():
                            setattr(existing_item, key, val)
                else:
                    new_item = doc.append('items', {})
                    for key, val in item_data.items():
                        setattr(new_item, key, val)

        doc.save()

        return {
            "status": 200,
            "message": "success",
            "data": doc
        }

    except frappe.DoesNotExistError:
        return {
            "status": 500,
            "message": f"Sales Invoice {docname} does not exist"
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
def delete_sales_invoice(docname):
    try:
        if not frappe.has_permission("Sales Invoice", "delete"):
            frappe.throw(("Not permitted"), frappe.PermissionError)

        doc = frappe.get_doc("Sales Invoice", docname)

        doc.delete()

        return {
            "status": 200,
            "message": "success"
        }

    except frappe.DoesNotExistError:
        return {
            "status": 500,
            "message": f"Sales Invoice {docname} does not exist"
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