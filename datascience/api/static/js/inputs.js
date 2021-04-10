const { 
    makeStyles,
    useTheme,
    TextField,
    FormControlLabel,
    Checkbox,
    FormControl,
    InputLabel,
    Select,
    MenuItem,
    KeyboardDatePicker,
    MuiPickersUtilsProvider,
    Input,
    List,
    ListItem,
    Accordion,
    AccordionSummary,
    AccordionDetails,
    AccordionActions,
    CardMedia,
} = MaterialUI;

const {
    useState,
    Fragment,
} = React;


const TYPES = {
    audio: AudioInput,
    bool: BooleanInput,
    categorical: CategoricalInput,
    date: DateInput,
    default: StringInput,
    email: EmailInput,
    float: FloatInput,
    image: ImageInput,
    int: IntegerInput,
    multiple: MultipleInput,
    str: StringInput,
    text: TextInput,
    url: UrlInput,
    video: VideoInput,
}


var inputs = {
    useStyles: makeStyles((theme) => ({
        formControl: {
            minWidth: '40ch',
        },
        button: {
            marginTop: theme.spacing(1),
        },
    })),
};


const render_input = metadata =>
    metadata.map(meta => select_input(meta))


function select_input(meta) {
    const dtype = meta.dtype.name
    const func = TYPES[dtype] || TYPES['default']
    return func(meta)
}


function ArrayInput() {
    return undefined
}


function StringInput({name}) {
    const {label, id} = get_labels(name, 'string')
return (
    <Fragment>
    <TextField
        id={ id }
        name={ label }  
        label={ label }
    />
    <br/>
    </Fragment>
)}


function TextInput({name}) {
    const {label, id} = get_labels(name, 'text')
return (
    <TextField 
        id={ id }
        name={ label }  
        label={ label }
        multiline
        rowsMax={4}
    />
)}


function IntegerInput({name}) {
    const {label, id} = get_labels(name, 'integer')
    const [shrink, setShrink] = useState(false);
    const [err, setErr] = useState(false);
return (
    <Fragment>
    <TextField
        type='number' 
        inputProps={{
            step: 1,
        }}

        id={ id } 
        name={ label }
        label={ label }

        onFocus={ event => setShrink(true) }

        onBlur={ event => setErr(() => {
            const val = event.target.value
            return val === '' | val != parseInt(val)
        })}

        error={ err }
        helperText={ err ? 'Integer values only' : '' }

        InputLabelProps={{
            shrink: shrink,
        }}
    />
    <br/>
    </Fragment>
)}


function FloatInput({name}) {
    const { label, id } = get_labels(name, 'float')
    const [shrink, setShrink] = useState(false);
    const [err, setErr] = useState(false);
return (
    <Fragment>
    <TextField 
        type='number' 
        inputProps={{
            step: 'any'
        }}

        id={ id }
        name={ label }
        label={ label }

        onFocus={ () => setShrink(true) }

        onBlur={ event => {
            const val = event.target.value;
            setErr(val === '')
        }}

        error={ err }
        helperText={ err ? 'Float values only' : '' }

        InputLabelProps={{
            shrink: shrink,
        }}
    />
    <br/>
    </Fragment>
)}


function BooleanInput({name}) { // TODO: reset has bugs
    const { label, id } = get_labels(name, 'boolean')
    const classes = inputs.useStyles();
return (
    <Fragment>
    <FormControlLabel
        label={ label }
        control={
            <Checkbox
            id={ id }
            name={ label }
            color="primary"
            />
        }
    />
    <br/>
    </Fragment>
)} 


function CategoricalInput({name, dtype}) {
    const { label, id } = get_labels(name, 'categorical')
    const classes = inputs.useStyles();
    const categories = dtype.args || ["cat 1", "cat 2", "cat 3"];
return(
    <Fragment>
    <FormControl 
        className={ classes.formControl }
    >
        <InputLabel id={ id + "-label" }>
            { label }
        </InputLabel>
        <Select
            id={ id }
            name={ label }
            labelId= { id + "-label" }
        >
        { categories.map( (cat, key) => {
                return <MenuItem 
                    key={ key }
                    value={ key }
                > 
                { cat.name }
                </MenuItem>
        })}
        </Select>
    </FormControl>
    <br/>
    </Fragment>
)}


function MultipleInput({name, dtype}) {
    const [keys, setKeys] = useState([]);
    
    const { label, id } = get_labels(name, 'categorical')
    const classes = inputs.useStyles();
    const theme = useTheme();
    
    const categories = dtype.args || ["c1", "c2", "c3"];

    const get_styles = (key, keys, theme) => ({
            fontWeight:
                keys.indexOf(key) === -1
                ? theme.typography.fontWeightRegular
                : theme.typography.fontWeightMedium,
    })

    const render_value = keys => {
        let vals = []
        for (const key of keys) {
            vals.push(cats[key])
        }
        return vals.join(', ') 
    }

    const menu_props = theme => ({
        PaperProps: {
            style: {
            maxHeight: 48 * 4.5 + 8,
            width: 250,
            },
        },
    })

return (
    <Fragment>
    <FormControl 
        className={ classes.formControl }
    >
        <InputLabel id={ id + "-label" }>
            { label }
        </InputLabel>

        <Select multiple
            id={ id }
            name={ label }
            labelId= { id + "-label" }

            input={ <Input /> }

            value={ keys }
            onChange={ event => setKeys(event.target.value.sort()) }
            renderValue={ render_value }
            MenuProps={ menu_props }
        >
        { categories.map((name, key) => (
            <MenuItem 
                key={ key } 
                value={ key } 
                style={ get_styles(key, keys, theme) }
            >
                { name }
            </MenuItem>
        ))}
        </Select>
    </FormControl>
    <br/>
    </Fragment>
)}


function DateInput({name}){ // requires DateFnsUtils
    const { label, id } = get_labels(name, 'date')
    const [date, setDate] = useState(new Date('2014-08-18T21:11:54'));
return(
    <MuiPickersUtilsProvider utils={DateFnsUtils}>
    <KeyboardDatePicker
        id={ id }
        name={ label }
        label={ label }

        disableToolbar
        variant="inline"
        format="yyyy/MM/dd"
        
        value={ date }
        onChange={ event => {setDate(event)}}

        margin="normal"
        KeyboardButtonProps={{
            'aria-label': 'change date',
        }}
    />
    </MuiPickersUtilsProvider>
)}


function EmailInput({name}){
    const { label, id } = get_labels(name, 'email')
    const [err, setErr] = useState(false)

    const on_blur = event => {
        const val = event.target.value
        setErr(val !== '' && !validate_email(val))
    }
    const text = err ? 'Invalid e-mail address' : ''
return(
    <TextField type='email'
        id={ id }
        name={ label }
        label={ label }
        error={ err }
        helperText={ text }
        onBlur={ on_blur }
    />
)}


function UrlInput({name}){
    const { label, id } = get_labels(name, 'url')
    const [err, setErr] = useState(false);

    const on_blur = event => {
        const val = event.target.value;
        setErr(val !== '' && !validate_url(val))
    }
    const text = err ? 'invalid URL' : ''
return(
    <TextField type='text'
        id={ id }
        name={ label }
        label={ label }
        error={ err }
        helperText={ text }
        onBlur={ on_blur }
    />
)}


function ImageInput({name, multiple}) {
    return FileInput({
        name: name,
        multiple: multiple,
        dtype: "image",
        accept: "image/*",
        render_file: (file, url) => (
            <img
                id={ file.name }
                src={ url }
                style={{ width: "100%" }}
            />
        )
    })
}


function AudioInput({name, multiple}) {
    return FileInput({
        name: name,
        multiple: multiple,
        dtype: "audio",
        accept: "audio/*",
        render_file: (file, url) => (
            <audio controls> 
            <source src={url} type={ file.type }/>
            </audio> 
        ),
    })
}


function VideoInput({name, multiple}) {
    return FileInput({
        name: name,
        multiple: multiple,
        dtype: "video",
        accept: "video/*",
        render_file: (file, url) => (
            <video controls style={{width: "100%"}}>
            <source src={ url } type={ file.type } />
            </video>
        ),
    })
}


function FileInput({name, dtype, accept, multiple, render_file}) {
    const {label, id} = get_labels(name, dtype)
    const [files, setFiles] = useState([])
    const [urls, setUrls] = useState([])
    const classes = inputs.useStyles()

    const on_change = event => {
        const files = [...event.target.files]
        files.forEach((file, key) => read_file(file, key))
        setFiles(files)
    }

    const read_file = (file, key) => {
        var reader = new FileReader();
        reader.onload = event => setUrls( prev => {
            const next = prev;
            next[key] = event.target.result
            return {...prev, ...next}
        })
        reader.readAsDataURL(file)
    }
return [
    <div>
    <Button
        className={ classes.button }
        variant="contained"
        component="label"
        >
        { label }
        <input type="file"
            hidden 
            id={ id } 
            name={ name }
            label={ label }
            accept= { accept } 
            multiple={ multiple }
            onChange={ on_change }
        />
    </Button>
    </div>
,
    files.length !== 0 && (
        <BreakCard>
        { files.map( (file, key) => (
            <Accordion 
                key={ key }
                TransitionProps={{ unmountOnExit: true }}
            >
                <AccordionSummary
                    raised={ 0 }
                    expandIcon={ <Icon>expand_more</Icon> }
                    aria-controls="panel1a-content"
                    id="panel1a-header"
                >
                    { file.name }
                </AccordionSummary>
                <AccordionDetails 
                    style={{ padding: 0 }}
                >
                    { render_file(file, urls[key]) }
                </AccordionDetails>
            <Divider />
                <AccordionActions>
                    { file.type } | { file.size }
                </AccordionActions>
            </Accordion>
        ))}
        </BreakCard>
    )
]}


// Helper functions

const get_labels = (name, dtype) => ({
    id: trim(['input', dtype, name || ''].join('-'),'-'),
    label: name || dtype,
})


function trim (s, c) {
    if (c === "]") c = "\\]";
    if (c === "^") c = "\\^";
    if (c === "\\") c = "\\\\";
    return s.replace(new RegExp(
        "^[" + c + "]+|[" + c + "]+$", "g"
    ), "");
}

function validate_email(email){
    // RFC 2822 compliant regex
    const re = /(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])/;
    return re.test(email);
}

function validate_url(url) {
    try {
        new URL(url);
        return true;
    } catch (_) {
      return false;  
    }
}


