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

        supplier = request_data.get('supplier')
        supplier_exists = frappe.get_all("Supplier", filters={"supplier_name": supplier})
        if not supplier_exists:
            new_supplier = frappe.new_doc('Supplier')
            new_supplier.supplier_name = supplier
            new_supplier.insert()

        credit_to_account = frappe.get_all("Account", filters={"account_number": request_data["credit_to"]})
        if credit_to_account:
            new_invoice = frappe.new_doc('Purchase Invoice')
            request_data["credit_to"] = credit_to_account[0].name
            for field, value in request_data.items():
                if field == 'items':
                    continue 
                if hasattr(new_invoice, field):
                    setattr(new_invoice, field, value)

            items_data = request_data.get('items', [])
            if items_data:
                for item_data in items_data:
                    expense_account = frappe.get_all("Account", filters={"account_number": item_data["expense_account"]})
                    if expense_account:
                        item_data["expense_account"] = expense_account[0].name
                        new_item = new_invoice.append('items', {})
                        for field, value in item_data.items():
                            setattr(new_item, field, value)
                    else:
                        return {
                            'status': 404,
                            'message': 'One or both accounts not found'
                        }


            new_invoice.insert()
            new_invoice.save()
            frappe.db.commit()

            # new_invoice.submit()

            return {
                'status': 200,
                'message': 'Purchase Invoice created successfully',
                'docname': new_invoice
            }
        
        else:
            return {
                'status': 404,
                'message': 'One or both accounts not found'
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

        if updates.get("credit_to"):
            credit_to_account = frappe.get_all("Account", filters={"account_number": updates["credit_to"]})
            if credit_to_account:
                credit_to_account = frappe.get_all("Account", filters={"account_number": updates["credit_to"]})
            else:
                return {
                    'status': 404,
                    'message': 'One or both accounts not found'
                } 

        for field, value in updates.items():
            if field == 'items':
                continue
            if hasattr(doc, field):
                setattr(doc, field, value)
            else:
                 return {
                    "status": 400,
                    "message": f"Field '{field}' either does not exist or cannot be modified"
                }

        items_data = updates.get('items', [])
        if items_data:
            for item_data in items_data:
                item_name = item_data.get('item_name')
                existing_item = next(
                        (item for item in doc.items if item.item_name == item_name), None
                    )
                if existing_item:
                    if item_data.get("expense_account"):
                        expense_account = frappe.get_all("Account", filters={"account_number": item_data["expense_account"]})
                        if expense_account:
                            item_data["expense_account"] = expense_account[0].name
                        else:
                            return {
                                'status': 404,
                                'message': 'Expense Account not Found'
                            }
                    
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

        paid_from_account = frappe.get_all("Account", filters={"account_number": request_data["paid_from"]})
        paid_to_account = frappe.get_all("Account", filters={"account_number": request_data["paid_to"]})

        if paid_from_account and paid_to_account:
            new_invoice = frappe.new_doc('Payment Entry')

            request_data["paid_from"] = paid_from_account[0].name
            request_data["paid_to"] = paid_to_account[0].name
            for field, value in request_data.items():
                if hasattr(new_invoice, field):
                    setattr(new_invoice, field, value)
                    
            new_invoice.insert()
            new_invoice.save()  

            frappe.db.commit()

            # new_invoice.submit()

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

        if updates.get('paid_from'):
            paid_from_account = frappe.get_all("Account", filters={"account_number": updates["paid_from"]})
            if paid_from_account:
                updates["paid_from"] = paid_from_account[0].name

        if updates.get('paid_to'):
            paid_to_account = frappe.get_all("Account", filters={"account_number": updates["paid_to"]})
            if paid_to_account:
                updates["paid_to"] = paid_to_account[0].name 

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

        customer = request_data.get('customer')
        customer_exists = frappe.get_all("Customer", filters={"customer_name": customer})
        if not customer_exists:
            new_customer = frappe.new_doc('Customer')
            new_customer.customer_name = customer
            new_customer.currency = "IDR"
            new_customer.insert()
       
        new_invoice = frappe.new_doc('Sales Invoice')
        for field, value in request_data.items():
            if field == 'items':
                continue
            if hasattr(new_invoice, field):
                setattr(new_invoice, field, value)
      
        items_data = request_data.get('items', [])
        if items_data: 
            for item_data in items_data:
                income_account = frappe.get_all("Account", filters={"account_number": item_data["income_account"] })
                debit_to_account = frappe.get_all("Account", filters={"account_number": item_data["debit_to"]})
                if income_account and debit_to_account:
                    item_data["income_account"] = income_account[0].name
                    item_data["debit_to_account"] = debit_to_account[0].name

                    new_item = new_invoice.append('items', {})
                    for field, value in item_data.items():
                        setattr(new_item, field, value)
                else:
                    return {
                        'status': 404,
                        'message': 'One or both accounts not found'
                    }

        new_invoice.insert()
        new_invoice.save()
        frappe.db.commit()
        # new_invoice.submit()
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
                item_name = item_data.get('item_name')
                existing_item = next(
                        (item for item in doc.items if item.item_name == item_name), None
                    )
                if existing_item:
                    if item_data.get("income_account"):
                        income_account = frappe.get_all("Account", filters={"account_number": item_data["income_account"] })
                        if income_account:
                            item_data["income_account"] = income_account[0].name
                        else:
                             return {
                                'status': 404,
                                'message': 'Income Account Not Found'
                            }

                    if item_data.get("debit_to"):
                        debit_to_account = frappe.get_all("Account", filters={"account_number": item_data["debit_to"]})
                        if debit_to_account:
                            item_data["debit_to_account"] = debit_to_account[0].name
                        else:
                            return {
                                'status': 404,
                                'message': 'Debut To Account not found'
                            }
                        
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


@frappe.whitelist()
def get_journal_entry():
    try:
        main_data = frappe.get_all('Journal Entry', fields=["*"])
        for entry in main_data:
            entry['accounts'] = frappe.get_all('Journal Entry Account', 
                                            filters={'parent': entry['name']},
                                            fields=["*"])

        response = {
            "status": 200,
            "message": "success",
            "data": main_data,
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), ("Journal Entry"))
        response = {
            "status": 500,
            "message": "Internal Server Error",
            "e":e
        }

    return response
 

@frappe.whitelist()
def get_journal_entry_by_id(docname):
    try:
        if not frappe.has_permission("Journal Entry", "read", doc=docname):
            frappe.throw(("Not permitted"), frappe.PermissionError)
        doc = frappe.get_doc("Journal Entry", docname)
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
def add_journal_entry():
    try:
        if not frappe.has_permission("Journal Entry", "create"):
            frappe.throw(("Not permitted"), frappe.PermissionError)

        request_data = frappe.request.json
       
        new_journal = frappe.new_doc('Journal Entry')
        for field, value in request_data.items():
            if field == 'accounts':
                continue
            if hasattr(new_journal, field):
                setattr(new_journal, field, value)
      
        accounts_data = request_data.get('accounts', [])
        if accounts_data: 
            for account_data in accounts_data:
                account = frappe.get_all("Account", filters={"account_number": account_data["account"]})
                if account:
                    account_data["account"] = account[0].name

                    new_item = new_journal.append('items', {})
                    for field, value in account_data.items():
                        setattr(new_item, field, value)
                else:
                    return {
                        'status': 404,
                        'message': 'Accounts not found'
                    }

        new_journal.insert()
        new_journal.save()
        frappe.db.commit()
        # new_invoice.submit()
        return {
            'status': 200,
            'message': 'Journal Entry created successfully',
            'docname': new_journal
        }

    except Exception as e:
        return {
            "status": 500,
            "message": "Internal Server Error",
            "e":e
        }


@frappe.whitelist()
def update_journal_entry(docname):
    try:
        data = frappe.request.json
        if not frappe.has_permission("Journal Entry", "write"):
            frappe.throw(("Not permitted"), frappe.PermissionError)

        docname = data.get('docname')
        updates = data.get('updates')

        doc = frappe.get_doc("Journal Entry", docname)

        for field, value in updates.items():
            if field == 'accounts':
                continue  # Skip 'items' field, handle it separately
            if hasattr(doc, field):
                setattr(doc, field, value)
            else:
                 return {
                    "status": 400,
                    "message": f"Field '{field}' either does not exist or cannot be modified"
                }

        accounts_data = updates.get('accounts', [])
        if accounts_data:  # Check if items_data is not empty
            for account_data in accounts_data:
                account_name = account_data.get('account')
                if account_data.get("account"):
                    account = frappe.get_all("Account", filters={"account_number": account_data["account"] })
                    if account:
                        account_data["income_account"] = account[0].name
                    else:
                        return {
                            'status': 404,
                            'message': 'Income Account Not Found'
                        }           
                existing_account = next(
                        (account for account in doc.accounts if account.account == account_name), None
                    )
                if existing_account:    
                    for key, val in account_data.items():
                        setattr(existing_account, key, val)
                else:
                    new_item = doc.append('accounts', {})
                    for key, val in account_data.items():
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
def delete_journal_entry(docname):
    try:
        if not frappe.has_permission("Journal Entry", "delete"):
            frappe.throw(("Not permitted"), frappe.PermissionError)

        doc = frappe.get_doc("Journal Entry", docname)

        doc.delete()

        return {
            "status": 200,
            "message": "success"
        }

    except frappe.DoesNotExistError:
        return {
            "status": 500,
            "message": f"Journal Entry {docname} does not exist"
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
def submit_journal_entry(docname):
    try:
        if not frappe.has_permission("Journal Entry", "write"):
            frappe.throw(("Not permitted"), frappe.PermissionError)

        doc = frappe.get_doc("Journal Entry", docname)
        if doc.docstatus == 0:
            doc.submit()

            return {
                'status': 200,
                'message': f'Journal Entry {docname} submitted successfully'
            }
        else:
            return {
                'status': 400,
                'message': f'Journal Entry {docname} is not in a draft state'
            }

    except frappe.DoesNotExistError:
        return {
            "status": 404,
            "message": f"Journal Entry {docname} does not exist"
        }

    except frappe.PermissionError:
        return {
            "status": 403,
            "message": "You don't have permission to submit this document"
        }

    except Exception as e:
        return {
            "status": 500,
            "message": "Internal Server Error",
            "e": e
        }

@frappe.whitelist()
def submit_purchase_invoice(docname):
    try:
        if not frappe.has_permission("Purchase Invoice", "write"):
            frappe.throw(("Not permitted"), frappe.PermissionError)

        doc = frappe.get_doc("Purchase Invoice", docname)
        if doc.docstatus == 0:
            doc.submit()

            return {
                'status': 200,
                'message': f'Purchase Invoice {docname} submitted successfully'
            }
        else:
            return {
                'status': 400,
                'message': f'Purchase Invoice {docname} is not in a draft state'
            }

    except frappe.DoesNotExistError:
        return {
            "status": 404,
            "message": f"Purchase Invoice {docname} does not exist"
        }

    except frappe.PermissionError:
        return {
            "status": 403,
            "message": "You don't have permission to submit this document"
        }

    except Exception as e:
        return {
            "status": 500,
            "message": "Internal Server Error",
            "e": e
        }


@frappe.whitelist()
def submit_sales_invoice(docname):
    try:
        if not frappe.has_permission("Sales Invoice", "write"):
            frappe.throw(("Not permitted"), frappe.PermissionError)

        doc = frappe.get_doc("Sales Invoice", docname)
        if doc.docstatus == 0:
            doc.submit()

            return {
                'status': 200,
                'message': f'Sales Invoice {docname} submitted successfully'
            }
        else:
            return {
                'status': 400,
                'message': f'Sales Invoice {docname} is not in a draft state'
            }

    except frappe.DoesNotExistError:
        return {
            "status": 404,
            "message": f"Sales Invoice {docname} does not exist"
        }

    except frappe.PermissionError:
        return {
            "status": 403,
            "message": "You don't have permission to submit this document"
        }

    except Exception as e:
        return {
            "status": 500,
            "message": "Internal Server Error",
            "e": e
        }

@frappe.whitelist()
def submit_payment_entry(docname):
    try:
        if not frappe.has_permission("Payment Entry", "write"):
            frappe.throw(("Not permitted"), frappe.PermissionError)

        doc = frappe.get_doc("Payment Entry", docname)
        if doc.docstatus == 0:
            doc.submit()

            return {
                'status': 200,
                'message': f'Payment Entry {docname} submitted successfully'
            }
        else:
            return {
                'status': 400,
                'message': f'Payment Entry {docname} is not in a draft state'
            }

    except frappe.DoesNotExistError:
        return {
            "status": 404,
            "message": f"Payment Entry {docname} does not exist"
        }

    except frappe.PermissionError:
        return {
            "status": 403,
            "message": "You don't have permission to submit this document"
        }

    except Exception as e:
        return {
            "status": 500,
            "message": "Internal Server Error",
            "e": e
        }