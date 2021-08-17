odoo.define('pos_receipt.pos_order_extend', function (require) {
    "use strict";
    var models = require('point_of_sale.models');

    var _super_posmodel = models.PosModel.prototype;
    models.PosModel = models.PosModel.extend({
        initialize: function (session, attributes) {
            // New code
            var partner_model = _.find(this.models, function (model) {
                return model.model === 'product.product';
            });
            partner_model.fields.push('warranty', 'year_type');
            // Inheritance
            return _super_posmodel.initialize.call(this, session, attributes);
        },
    });


    models.Orderline = models.Orderline.extend(
        {
            get_warranty: function () {
                return this.product.warranty;
            },

             get_year_type: function () {
                return this.product.year_type;
            },
            export_for_printing: function () {
                console.log("Product Name: " + this.get_product().display_name);
                console.log("Warranty: " + this.get_warranty());
                console.log("year: " + this.get_year_type());
                return {
                    id: this.id,
                    quantity: this.get_quantity(),
                    unit_name: this.get_unit().name,
                    price: this.get_unit_display_price(),
                    discount: this.get_discount(),
                    product_name: this.get_product().display_name,
                    product_name_wrapped: this.generate_wrapped_product_name(),
                    price_lst: this.get_lst_price(),
                    display_discount_policy: this.display_discount_policy(),
                    price_display_one: this.get_display_price_one(),
                    price_display: this.get_display_price(),
                    price_with_tax: this.get_price_with_tax(),
                    price_without_tax: this.get_price_without_tax(),
                    price_with_tax_before_discount: this.get_price_with_tax_before_discount(),
                    tax: this.get_tax(),
                    product_description: this.get_product().description,
                    product_description_sale: this.get_product().description_sale,
                    warranty: this.get_warranty(),
                    year_type: this.get_year_type(),
                    // year_type: this.get_warranty(),
                };
            },
        }
    )
});