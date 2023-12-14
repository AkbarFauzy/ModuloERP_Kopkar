import frappe

@frappe.whitelist()
def get_pembelian_stnk():
    return frappe.db.sql(f"""SELECT * FROM `tabSTNK`; """, as_dict=True)

def get_pembelian_stnk_by_id(id):
    return 

def get_penjualan_stnk():
    return
