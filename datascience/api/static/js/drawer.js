const {

    makeStyles,
    Drawer,
    Button,
    List,
    Divider,
    ListItem,
    ListItemIcon,
    ListItemText,

} = MaterialUI

const drawerWidth = 250

var drawer = {
    useStyles: makeStyles( theme => ({
        list: {
            width: drawerWidth,
        },
        fullList: {
            width: 'auto',
        },
        menuButton: {
            marginRight: theme.spacing(2),
        },
        toolbar: theme.mixins.toolbar,
            drawerPaper: {
                width: drawerWidth,
        },
    }))
}


function MainDrawer({sitemap}) {
    const classes = drawer.useStyles()
    const theme = useTheme()
    const dark = theme.palette.type == "dark"

    const [state, setState] = React.useState({open: false});

    const toggleDrawer = open => event => {
        if (
            event.type === 'keydown' 
            && (event.key === 'Tab' || event.key === 'Shift')
        ) {
            return
        }
        setState({ ...state, ["open"]: open })
    };

    const list = (
        <div
            className={ classes.list }
            role="presentation"
            onClick={ toggleDrawer(false) }
            onKeyDown={ toggleDrawer(false) }
        >
        <div className={ classes.toolbar } />
        <Divider />
        <List>
        { sitemap.map( item => (

            <ListItem
                button
                component='a'
                href={ item.url }
                key={ item.name }
            >

            <ListItemIcon>
                { item.name.toLowerCase() == 'home'
                    ? <Icon> home </Icon>
                    : <Icon> send </Icon>
                }
            </ListItemIcon>

            <ListItemText primary={ item.name } />
            
            </ListItem>
        
        ))}
        </List>
        </div>
    )


return (

<div>
<IconButton 
    className={ classes.menuButton } 
    onClick={ toggleDrawer(true) }
    edge="start" 
    color="inherit"
    aria-label="menu"
>
    <Icon> menu </Icon>
</IconButton>

<Drawer 
    anchor="left" 
    open={ state["open"] }
    onClose={ toggleDrawer(false) }
>
    <Divider />
    { list }
    
</Drawer>
</div>

)}
