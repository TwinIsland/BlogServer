const std = @import("std");
const sqlite3 = @import("sqlite3.zig");

pub fn main() !void {
    defer {
        sqlite3.close_db() catch |err| {
            std.debug.print("Encountered an error: {}\n", .{err});
        };
    }

    _ = sqlite3.load_db("test.db");

    const query = "SELECT * FROM blog;";

    try sqlite3.execute(query);
}
