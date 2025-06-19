from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Demo")

@mcp.tool()
def read_quota() -> str:
    """Reads the quota amount"""
    with open("../../quota.txt", "r") as f:
        return f.read()

@mcp.tool()
def set_quota(amount: int) -> str:
    """Sets the quota amount"""
    with open("../../quota.txt", "w") as f:
        f.write(str(amount))
    return amount

if __name__ == "__main__":
    mcp.run(transport="sse")
