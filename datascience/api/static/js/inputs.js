const { 
    makeStyles, useTheme, TextField, FormControlLabel, Checkbox,
    FormControl, InputLabel, Select, MenuItem, KeyboardDatePicker,
    MuiPickersUtilsProvider, Input, List, ListItem, Accordion,
    AccordionSummary, AccordionDetails, AccordionActions, CardMedia,
} = MaterialUI;


const { useState, Fragment } = React;


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


const render_input = metadata => metadata.map(select_input)


function select_input(field) {
    const dtype = field.dtype
    const name = typeof dtype === "string" ? dtype : dtype.name
    const func = TYPES[name] || TYPES['default']
    return func(field)
}


function StringInput({name, value, required, defaultValue}) {
    const {label, id} = get_labels(name, 'string')
return (
    <Fragment key={ id }>
    <TextField
        id={ id }
        name={ label }  
        label={ label }
        required={ !!required }
        defaultValue={ get_default(value, required, defaultValue) }
    />
    <br/>
    <br />
    </Fragment>
)}


function TextInput({name, value, required, defaultValue}) {
    const {label, id} = get_labels(name, 'text')
return (
    <Fragment key={ id }>
    <TextField 
        multiline
        rowsMax={4}
        id={ id }
        name={ label }  
        label={ label }
        required={ !!required }
        defaultValue={ get_default(value, required, defaultValue) }
    />
    <br/>
    <br />
    </Fragment>
)}


function IntegerInput({name, value, required, defaultValue}) {
    const {label, id} = get_labels(name, 'integer')
    const [shrink, setShrink] = useState(
        value !== null || (!required && defaultValue !== null)
    )
    const [err, setErr] = useState(false)
return (
    <Fragment key={ id }>
    <TextField
        type='number' 
        inputProps={{
            step: 1,
        }}

        id={ id } 
        name={ label }
        label={ label } 

        required={ !!required }
        defaultValue={ get_default(value, required, defaultValue) }

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
    <br />
    </Fragment>
)}


function FloatInput({name, value, required, defaultValue}) {
    const { label, id } = get_labels(name, 'float')
    const [shrink, setShrink] = useState(
        value !== null || (!required && defaultValue !== null)
    )
    const [err, setErr] = useState(false)
return (
    <Fragment key={ id }>
    <TextField 
        type='number' 
        inputProps={{
            step: 'any'
        }}

        id={ id }
        name={ label }
        label={ label }
        required={ !!required }
        defaultValue={ get_default(value, required, defaultValue) }

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
    <br />
    </Fragment>
)}


function BooleanInput({name, value, defaultValue}) {
    // TODO: reset ?!
    const { label, id } = get_labels(name, 'boolean')
    const classes = inputs.useStyles()
    const [checked, setChecked] = useState(value !== null ? value : !!defaultValue)

return (
    <Fragment key={ id }>
    <FormControlLabel
        label={ label }
        control={
            <Checkbox
            id={ id }
            name={ label }
            color="primary"
            checked={ checked }
            onChange={ event => setChecked(event.target.checked) }
            />
        }
    />
    <br />
    </Fragment>
)} 


function CategoricalInput({name, value, dtype, required, defaultValue}) {
    const { label, id } = get_labels(name, 'categorical')
    const categories = dtype.args || ["cat 1", "cat 2", "cat 3"]
    const classes = inputs.useStyles()
return(
    <Fragment key={ id }>
    <FormControl 
        className={ classes.formControl }
        required={ !!required }
        >
        <InputLabel id={ id + "-label" }>
            { label }
        </InputLabel>
        <Select
            id={ id }
            name={ label }
            labelId={ id + "-label" }
            defaultValue={ get_default(value, required, defaultValue) }
        >
        { required 
            ? null
            : <MenuItem value={ null }><em>none</em></MenuItem>
        }
        { categories.map( (cat, key) => {
            return <MenuItem 
                key={ key }
                value={ key }
            > 
            { cat }
            </MenuItem>
        })}
        </Select>
    </FormControl>
    <br />
    </Fragment>
)}


function MultipleInput({name, value, dtype, required, defaultValue}) {
    const {label, id} = get_labels(name, 'multiple')
    const categories = dtype.args || ["c1", "c2", "c3"]
    
    const [keys, setKeys] = useState([])

    const theme = useTheme()
    const classes = inputs.useStyles()

    const get_styles = (key, keys, theme) => ({
            fontWeight:
                keys.indexOf(key) === -1
                ? theme.typography.fontWeightRegular
                : theme.typography.fontWeightMedium,
    })

    const render_value = keys => {
        let vals = []
        for (const key of keys) {
            vals.push(categories[key])
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
    <Fragment key={ id }>
    <FormControl 
        className={ classes.formControl }
        required={ !!required }
    >
        <InputLabel id={ id + "-label" }>
            { label }
        </InputLabel>

        <Select multiple
            id={ id }
            name={ label }
            labelId= { id + "-label" }
            // TODO: fix default value
            defaultValue={ get_default(value, required, defaultValue) }

            input={ <Input /> }

            value={ keys || undefined }
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
    <br />
    </Fragment>
)}


function DateInput({name, required, defaultValue}){ // requires DateFnsUtils
    const { label, id } = get_labels(name, 'date')
    const [date, setDate] = useState(new Date('2014-08-18T21:11:54'));
return(
    <MuiPickersUtilsProvider utils={DateFnsUtils}>
    <KeyboardDatePicker
        id={ id }
        name={ label }
        label={ label }
        required={ !!required }
        defaultValue={ get_default(value, required, defaultValue) }
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


function EmailInput({name, required, defaultValue}){
    const { label, id } = get_labels(name, 'email')
    const [err, setErr] = useState(false)

    const on_blur = event => {
        const val = event.target.value
        setErr(val !== '' && !validate_email(val))
    }
    const text = err ? 'Invalid e-mail address' : ''
return(
    <Fragment key={ id }>
    <TextField type='email'
        id={ id }
        name={ label }
        label={ label }
        required={ !!required }
        defaultValue={ get_default(value, required, defaultValue) }
        error={ err }
        helperText={ text }
        onBlur={ on_blur }
    />
    <br />
    </Fragment>
)}


function UrlInput({name, required, defaultValue}){
    const { label, id } = get_labels(name, 'url')
    const [err, setErr] = useState(false);

    const on_blur = event => {
        const val = event.target.value;
        setErr(val !== '' && !validate_url(val))
    }
    const text = err ? 'invalid URL' : ''
return(
    <Fragment key={ id }>
    <TextField type='text'
        id={ id }
        name={ label }
        label={ label }
        required={ !!required }
        defaultValue={ get_default(value, required, defaultValue) }
        error={ err }
        helperText={ text }
        onBlur={ on_blur }
    />
    <br />
    </Fragment>
)}


function ImageInput({name, multiple, required}) {
    return FileInput({
        name: name,
        multiple: multiple,
        required: required,
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


function AudioInput({name, multiple, required}) {
    return FileInput({
        name: name,
        multiple: multiple,
        required: required,
        dtype: "audio",
        accept: "audio/*",
        render_file: (file, url) => (
            <audio controls> 
            <source src={url} type={ file.type }/>
            </audio> 
        ),
    })
}


function VideoInput({name, multiple, required}) {
    return FileInput({
        name: name,
        multiple: multiple,
        required: required,
        dtype: "video",
        accept: "video/*",
        render_file: (file, url) => (
            <video controls style={{width: "100%"}}>
            <source src={ url } type={ file.type } />
            </video>
        ),
    })
}


function FileInput({name, dtype, accept, multiple, required, render_file}) {
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
    <Fragment key={ id }>
    <Button
        className={ classes.button }
        variant="contained"
        color="secondary"
        component="label"
    >
        { label }
        <input type="file"
            hidden 
            id={ id } 
            name={ name }
            label={ label }
            required={ !!required }
            accept= { accept } 
            multiple={ multiple }
            onChange={ on_change }
        />
    </Button>
    <br />
    </Fragment>
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

function get_default(value, required, defaultValue){
    const dvalue = !required && defaultValue !== null ? defaultValue : ''
    return value !== null ? value : dvalue
}


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


