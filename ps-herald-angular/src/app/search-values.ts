export class Searchvalues {
    public system_id: string = "not_selected";
    public sub_system_id: string = "not_selected";
    public sub_sub_system_id: string = "not_selected";
    public user_spec_1: string = "not_selected";
    public user_spec_2: string = "not_selected";
    public produkt_id: string = "not_selected";
    public pattern: string = "not_selected";
    public starting_at: string = "not_selected";
    public notify_level: string = "10";
    public num_records: string = "10";
    public order: string = "desc";


    state() {
        let state: string[] = [];
        state.push("system_id: " + this.system_id);
        state.push("sub_system_id: " + this.sub_system_id);
        state.push("sub_sub_system_id: " + this.sub_sub_system_id);
        state.push("user_spec_1: " + this.user_spec_1);
        state.push("user_spec_2: " + this.user_spec_2);
        state.push("produkt_id: " + this.produkt_id);
        state.push("pattern: " + this.pattern);
        state.push("starting_at: " + this.starting_at);
        state.push("notify_level: " + this.notify_level);
        state.push("num_records: " + this.num_records);
        state.push("order: " + this.order);
        return state;
    }

    constructor() { }

}
export class SearchOptions {
    public system_ids: [string] = ["not_selected"];
    public sub_system_ids: [string] = ["not_selected"];
    public sub_sub_system_ids: [string] = ["not_selected"];
    public user_spec_1s: [string] = ["not_selected"];
    public user_spec_2s: [string] = ["not_selected"];
    public product_ids: [string] = ["not_selected"];
    public notify_levels = [];
    public orders = [];
    constructor(
    ) {
        this.notify_levels.push({ "key": "ALL(>00)", "value": "100" });
        this.notify_levels.push({ "key": "DEBUG(>10)", "value": "10" });
        this.notify_levels.push({ "key": "INFO(>20)", "value": "20" });
        this.notify_levels.push({ "key": "ERROR(>30)", "value": "30" });
        this.orders.push({ "key": "Newest Log Record First", "value": "desc" });
        this.orders.push({ "key": "Oldest Log Record First", "value": "asc" });
    }
}