-- =============================================================================
-- O2C Graph System Database Schema
-- SQLite3
-- =============================================================================

-- Sales Order Headers
CREATE TABLE IF NOT EXISTS sales_order_headers (
    salesOrder TEXT PRIMARY KEY,
    salesOrderType TEXT,
    salesOrganization TEXT,
    distributionChannel TEXT,
    organizationDivision TEXT,
    salesGroup TEXT,
    salesOffice TEXT,
    soldToParty TEXT,
    creationDate TEXT,
    createdByUser TEXT,
    lastChangeDateTime TEXT,
    totalNetAmount REAL,
    overallDeliveryStatus TEXT,
    overallOrdReltdBillgStatus TEXT,
    overallSdDocReferenceStatus TEXT,
    transactionCurrency TEXT,
    pricingDate TEXT,
    requestedDeliveryDate TEXT,
    headerBillingBlockReason TEXT,
    deliveryBlockReason TEXT,
    incotermsClassification TEXT,
    incotermsLocation1 TEXT,
    customerPaymentTerms TEXT,
    totalCreditCheckStatus TEXT
);

-- Sales Order Items
CREATE TABLE IF NOT EXISTS sales_order_items (
    salesOrder TEXT,
    salesOrderItem TEXT,
    material TEXT,
    materialGroup TEXT,
    requestedQuantity REAL,
    requestedQuantityUnit TEXT,
    netAmount REAL,
    transactionCurrency TEXT,
    productionPlant TEXT,
    storageLocation TEXT,
    salesOrderItemCategory TEXT,
    itemBillingBlockReason TEXT,
    salesDocumentRjcnReason TEXT,
    PRIMARY KEY (salesOrder, salesOrderItem),
    FOREIGN KEY (salesOrder) REFERENCES sales_order_headers(salesOrder)
);

-- Billing Document Headers
CREATE TABLE IF NOT EXISTS billing_document_headers (
    billingDocument TEXT PRIMARY KEY,
    billingDocumentType TEXT,
    accountingDocument TEXT,
    soldToParty TEXT,
    billingDocumentDate TEXT,
    creationDate TEXT,
    creationTime TEXT,
    lastChangeDateTime TEXT,
    totalNetAmount REAL,
    transactionCurrency TEXT,
    billingDocumentIsCancelled INTEGER,
    cancelledBillingDocument TEXT,
    companyCode TEXT,
    fiscalYear INTEGER
);

-- Billing Document Items
CREATE TABLE IF NOT EXISTS billing_document_items (
    billingDocument TEXT,
    billingDocumentItem TEXT,
    material TEXT,
    billingQuantity REAL,
    billingQuantityUnit TEXT,
    netAmount REAL,
    transactionCurrency TEXT,
    referenceSdDocument TEXT,
    referenceSdDocumentItem TEXT,
    PRIMARY KEY (billingDocument, billingDocumentItem),
    FOREIGN KEY (billingDocument) REFERENCES billing_document_headers(billingDocument)
);

-- Billing Document Cancellations
CREATE TABLE IF NOT EXISTS billing_document_cancellations (
    billingDocument TEXT PRIMARY KEY,
    billingDocumentType TEXT,
    accountingDocument TEXT,
    soldToParty TEXT,
    billingDocumentDate TEXT,
    creationDate TEXT,
    creationTime TEXT,
    lastChangeDateTime TEXT,
    totalNetAmount REAL,
    transactionCurrency TEXT,
    billingDocumentIsCancelled INTEGER,
    cancelledBillingDocument TEXT,
    companyCode TEXT,
    fiscalYear INTEGER
);

-- Outbound Delivery Headers
CREATE TABLE IF NOT EXISTS outbound_delivery_headers (
    deliveryDocument TEXT PRIMARY KEY,
    creationDate TEXT,
    creationTime TEXT,
    lastChangeDate TEXT,
    actualGoodsMovementDate TEXT,
    actualGoodsMovementTime TEXT,
    overallGoodsMovementStatus TEXT,
    overallPickingStatus TEXT,
    overallProofOfDeliveryStatus TEXT,
    deliveryBlockReason TEXT,
    headerBillingBlockReason TEXT,
    hdrGeneralIncompletionStatus TEXT,
    shippingPoint TEXT
);

-- Journal Entry Items (Accounts Receivable)
CREATE TABLE IF NOT EXISTS journal_entry_items_accounts_receivable (
    accountingDocument TEXT,
    accountingDocumentItem TEXT,
    companyCode TEXT,
    fiscalYear INTEGER,
    referenceDocument TEXT,
    customer TEXT,
    glAccount TEXT,
    costCenter TEXT,
    profitCenter TEXT,
    amountInTransactionCurrency REAL,
    transactionCurrency TEXT,
    amountInCompanyCodeCurrency REAL,
    companyCodeCurrency TEXT,
    postingDate TEXT,
    documentDate TEXT,
    clearingDate TEXT,
    clearingAccountingDocument TEXT,
    clearingDocFiscalYear INTEGER,
    accountingDocumentType TEXT,
    financialAccountType TEXT,
    assignmentReference TEXT,
    lastChangeDateTime TEXT,
    PRIMARY KEY (accountingDocument, accountingDocumentItem)
);

-- Payments (Accounts Receivable)
CREATE TABLE IF NOT EXISTS payments_accounts_receivable (
    accountingDocument TEXT,
    accountingDocumentItem TEXT,
    companyCode TEXT,
    fiscalYear INTEGER,
    invoiceReference TEXT,
    invoiceReferenceFiscalYear INTEGER,
    customer TEXT,
    salesDocument TEXT,
    salesDocumentItem TEXT,
    glAccount TEXT,
    amountInTransactionCurrency REAL,
    transactionCurrency TEXT,
    amountInCompanyCodeCurrency REAL,
    companyCodeCurrency TEXT,
    postingDate TEXT,
    documentDate TEXT,
    clearingDate TEXT,
    clearingAccountingDocument TEXT,
    clearingDocFiscalYear INTEGER,
    financialAccountType TEXT,
    assignmentReference TEXT,
    costCenter TEXT,
    profitCenter TEXT,
    PRIMARY KEY (accountingDocument, accountingDocumentItem)
);

-- Business Partners
CREATE TABLE IF NOT EXISTS business_partners (
    businessPartner TEXT PRIMARY KEY,
    customer TEXT UNIQUE,
    businessPartnerFullName TEXT,
    businessPartnerName TEXT,
    firstName TEXT,
    lastName TEXT,
    formOfAddress TEXT,
    businessPartnerCategory TEXT,
    businessPartnerGrouping TEXT,
    correspondenceLanguage TEXT,
    industry TEXT,
    organizationBpName1 TEXT,
    organizationBpName2 TEXT,
    businessPartnerIsBlocked INTEGER,
    isMarkedForArchiving INTEGER,
    creationDate TEXT,
    creationTime TEXT,
    createdByUser TEXT,
    lastChangeDate TEXT
);

-- Customer Company Assignments
CREATE TABLE IF NOT EXISTS customer_company_assignments (
    customer TEXT,
    companyCode TEXT,
    customerAccountGroup TEXT,
    paymentTerms TEXT,
    paymentMethodsList TEXT,
    paymentBlockingReason TEXT,
    accountingClerk TEXT,
    accountingClerkPhoneNumber TEXT,
    accountingClerkFaxNumber TEXT,
    accountingClerkInternetAddress TEXT,
    reconciliationAccount TEXT,
    alternativePayerAccount TEXT,
    deletionIndicator INTEGER,
    PRIMARY KEY (customer, companyCode)
);

-- Customer Sales Area Assignments
CREATE TABLE IF NOT EXISTS customer_sales_area_assignments (
    customer TEXT,
    salesOrganization TEXT,
    distributionChannel TEXT,
    division TEXT,
    salesGroup TEXT,
    salesOffice TEXT,
    salesDistrict TEXT,
    customerPaymentTerms TEXT,
    billingIsBlockedForCustomer INTEGER,
    completeDeliveryIsDefined INTEGER,
    deliveryPriority TEXT,
    incotermsClassification TEXT,
    incotermsLocation1 TEXT,
    shippingCondition TEXT,
    supplyingPlant TEXT,
    currency TEXT,
    exchangeRateType TEXT,
    creditControlArea TEXT,
    slsUnlmtdOvrdelivIsAllwd INTEGER,
    PRIMARY KEY (customer, salesOrganization, distributionChannel, division)
);

-- Product Descriptions
CREATE TABLE IF NOT EXISTS product_descriptions (
    product TEXT PRIMARY KEY,
    language TEXT,
    productDescription TEXT
);

-- Plants
CREATE TABLE IF NOT EXISTS plants (
    plant TEXT PRIMARY KEY,
    plantName TEXT,
    plantCategory TEXT,
    addressId TEXT,
    valuationArea TEXT,
    factoryCalendar TEXT,
    salesOrganization TEXT,
    distributionChannel TEXT,
    division TEXT,
    language TEXT,
    plantCustomer TEXT,
    plantSupplier TEXT,
    defaultPurchasingOrganization TEXT,
    isMarkedForArchiving INTEGER
);

-- Product Plants
CREATE TABLE IF NOT EXISTS product_plants (
    product TEXT,
    plant TEXT,
    mrpType TEXT,
    availabilityCheckType TEXT,
    fiscalYearVariant TEXT,
    profitCenter TEXT,
    countryOfOrigin TEXT,
    regionOfOrigin TEXT,
    productionInvtryManagedLoc TEXT,
    PRIMARY KEY (product, plant)
);

-- Product Storage Locations
CREATE TABLE IF NOT EXISTS product_storage_locations (
    product TEXT,
    plant TEXT,
    storageLocation TEXT,
    physicalInventoryBlockInd TEXT,
    dateOfLastPostedCntUnRstrcdStk TEXT,
    PRIMARY KEY (product, plant, storageLocation)
);

-- Sales Order Schedule Lines
CREATE TABLE IF NOT EXISTS sales_order_schedule_lines (
    salesOrder TEXT,
    salesOrderItem TEXT,
    scheduleLine TEXT,
    orderQuantityUnit TEXT,
    confdOrderQtyByMatlAvailCheck REAL,
    confirmedDeliveryDate TEXT,
    PRIMARY KEY (salesOrder, salesOrderItem, scheduleLine)
);

-- =============================================================================
-- Indexes for Foreign Key Columns
-- =============================================================================
CREATE INDEX IF NOT EXISTS idx_soh_soldto ON sales_order_headers(soldToParty);
CREATE INDEX IF NOT EXISTS idx_soi_salesorder ON sales_order_items(salesOrder);
CREATE INDEX IF NOT EXISTS idx_soi_material ON sales_order_items(material);
CREATE INDEX IF NOT EXISTS idx_soi_plant ON sales_order_items(productionPlant);

CREATE INDEX IF NOT EXISTS idx_bdh_soldto ON billing_document_headers(soldToParty);
CREATE INDEX IF NOT EXISTS idx_bdh_accdoc ON billing_document_headers(accountingDocument);
CREATE INDEX IF NOT EXISTS idx_bdi_material ON billing_document_items(material);
CREATE INDEX IF NOT EXISTS idx_bdi_refsddoc ON billing_document_items(referenceSdDocument);

CREATE INDEX IF NOT EXISTS idx_je_accdoc ON journal_entry_items_accounts_receivable(accountingDocument);
CREATE INDEX IF NOT EXISTS idx_je_customer ON journal_entry_items_accounts_receivable(customer);
CREATE INDEX IF NOT EXISTS idx_je_refdoc ON journal_entry_items_accounts_receivable(referenceDocument);

CREATE INDEX IF NOT EXISTS idx_par_accdoc ON payments_accounts_receivable(accountingDocument);
CREATE INDEX IF NOT EXISTS idx_par_customer ON payments_accounts_receivable(customer);
CREATE INDEX IF NOT EXISTS idx_par_invoice ON payments_accounts_receivable(invoiceReference);
